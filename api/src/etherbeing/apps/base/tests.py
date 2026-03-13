from io import StringIO
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.base.models import BlogEntry, Configuration, Project, PublishedPost, Service, SiteContent
from apps.base.models import ContactMessage, ContactThread
from apps.base.seed_data import initialize_configuration, initialize_site_content


class SiteContentSeedTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_initialize_site_content_creates_singleton_with_related_records(self):
        site_content = initialize_site_content()

        self.assertEqual(site_content.slug, "primary")
        self.assertEqual(SiteContent.objects.count(), 1)
        self.assertEqual(Configuration.objects.count(), 1)
        self.assertEqual(site_content.about_highlights.count(), 4)
        self.assertEqual(site_content.skills.count(), 6)
        self.assertEqual(site_content.services.count(), 13)
        self.assertEqual(site_content.contact_groups.count(), 3)
        self.assertEqual(site_content.contact_groups.first().links.count(), 7)
        self.assertEqual(site_content.gallery_photos.count(), 1)
        self.assertEqual(site_content.featured_chart_symbol, "BITSTAMP:ETHUSD")
        self.assertIn("blog_integrations", site_content.strategy_business_idea)

    def test_initialize_site_content_is_idempotent(self):
        first = initialize_site_content()
        first.about_highlights.first().delete()

        second = initialize_site_content()

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(second.about_highlights.count(), 4)
        self.assertEqual(SiteContent.objects.count(), 1)
        self.assertEqual(second.services.count(), 13)
        self.assertEqual(second.gallery_photos.count(), 1)

    def test_management_command_initializes_site_content(self):
        stdout = StringIO()

        call_command("init_site_content", stdout=stdout)

        self.assertEqual(SiteContent.objects.count(), 1)
        self.assertIn("initialized successfully", stdout.getvalue())

    def test_initialize_configuration_is_idempotent(self):
        first = initialize_configuration()
        first.site_name = "Changed"
        first.save()

        second = initialize_configuration()

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(second.site_name, "etherbeing")


class SiteContentApiTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_site_content_endpoint_bootstraps_when_missing(self):
        response = self.client.get("/api/site/content/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["site_title"], "etherbeing")
        self.assertEqual(payload["configuration"]["favicon_url"], "https://etherbeing.github.io/favicon.png")
        self.assertEqual(len(payload["about_highlights"]), 4)
        self.assertEqual(payload["skills"][0]["image_url"], "/skills/kali.png")
        self.assertTrue(payload["skills"][0]["headline"])
        self.assertTrue(payload["skills"][0]["description"])
        self.assertEqual(payload["featured_chart_symbol"], "BITSTAMP:ETHUSD")
        self.assertEqual(payload["featured_chart_title"], "Ethereum / USD")
        self.assertEqual(len(payload["gallery_photos"]), 1)
        self.assertEqual(SiteContent.objects.count(), 1)

    def test_site_content_endpoint_includes_featured_projects_and_blog_entries(self):
        initialize_site_content()
        Project.objects.create(
            github_id="123",
            name="etherbeing-site",
            description="Personal website",
            stargazers_count=9,
            watchers_count=4,
            html_url="https://github.com/etherbeing/etherbeing_official",
            language="TypeScript",
        )
        BlogEntry.objects.create(
            gist_id="gist-1",
            description="Dynamic content post",
            content="# Hello",
            html_url="https://gist.github.com/etherbeing/gist-1",
        )

        response = self.client.get("/api/site/content/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["featured_projects"][0]["name"], "etherbeing-site")
        self.assertEqual(payload["featured_blog_entries"][0]["gist_id"], "gist-1")
        self.assertEqual(payload["contact_groups"][0]["title"], "Social Networks")
        self.assertIn(
            "TradingView",
            [link["label"] for link in payload["contact_groups"][0]["links"]],
        )

    def test_site_content_endpoint_uses_cache(self):
        initialize_site_content()

        with patch("apps.base.controllers.initialize_site_content") as initialize_mock:
            first_response = self.client.get("/api/site/content/")
            second_response = self.client.get("/api/site/content/")

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        initialize_mock.assert_not_called()

    def test_site_content_endpoint_normalizes_legacy_cached_payload(self):
        cache.set(
            "site-content",
            {
                "site_title": "etherbeing",
                "hero_titles": [],
                "hero_summary": "",
                "hero_cta_label": "Download CV",
                "hero_cta_url": "/cv.pdf",
                "about_short_bio": "",
                "buy_me_a_coffee_url": "",
                "contact_intro": "",
                "footer_copy": "",
                "footer_tagline": "",
                "featured_chart_symbol": "",
                "featured_chart_title": "",
                "about_highlights": [],
                "skills": [],
                "services": [],
                "contact_groups": [],
                "gallery_photos": [],
                "featured_projects": [],
                "featured_blog_entries": [],
            },
            timeout=60,
        )

        response = self.client.get("/api/site/content/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["strategy_business_idea"]["blog_integrations"],
            [],
        )
        self.assertEqual(response.json()["featured_chart_symbol"], "BITSTAMP:ETHUSD")
        self.assertEqual(response.json()["gallery_photos"], [])

    def test_configuration_endpoint_bootstraps_configuration(self):
        response = self.client.get("/api/site/configuration/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["site_name"], "etherbeing")
        self.assertEqual(payload["favicon_url"], "https://etherbeing.github.io/favicon.png")
        self.assertEqual(Configuration.objects.count(), 1)

    def test_service_detail_endpoint_returns_seeded_service(self):
        initialize_site_content()

        response = self.client.get("/api/site/service/frontend-web-development/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["slug"], "frontend-web-development")
        self.assertEqual(payload["title"], "Frontend Web Development")
        self.assertTrue(payload["deliverables"])
        self.assertTrue(payload["process_steps"])

    def test_service_detail_endpoint_rebuilds_services_when_site_content_exists_without_them(self):
        site_content = initialize_site_content()
        site_content.services.all().delete()

        response = self.client.get("/api/site/service/frontend-web-development/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slug"], "frontend-web-development")
        self.assertTrue(Service.objects.filter(slug="frontend-web-development").exists())

    def test_service_request_requires_authenticated_user(self):
        initialize_site_content()

        response = self.client.post(
            "/api/site/service/frontend-web-development/request/",
            {"message": "I need a secure marketing site."},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_service_request_creates_pending_request_for_logged_in_user(self):
        initialize_site_content()
        user = get_user_model().objects.create_user(
            username="reader-user",
            email="reader@example.com",
            github_login="reader-user",
            github_access_token="front-access-token",
            github_token_scope="read:user,user:email",
        )
        self.client.force_login(user)

        response = self.client.post(
            "/api/site/service/frontend-web-development/request/",
            {"message": "I need a secure marketing site."},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["status"], "pending")
        self.assertEqual(payload["service"]["slug"], "frontend-web-development")
        self.assertEqual(payload["requester"]["username"], "reader-user")
        self.assertEqual(payload["message"], "I need a secure marketing site.")

    def test_contact_threads_requires_authenticated_user(self):
        response = self.client.get("/api/site/contact/threads/")
        self.assertEqual(response.status_code, 401)

    @override_settings(
        RECAPTCHA_SITE_KEY="",
        RECAPTCHA_SECRET_KEY="",
    )
    def test_authenticated_user_can_create_contact_thread(self):
        user = get_user_model().objects.create_user(
            username="contact-user",
            email="contact@example.com",
            github_login="contact-user",
            github_access_token="front-access-token",
            github_token_scope="read:user,user:email",
        )
        self.client.force_login(user)

        response = self.client.post(
            "/api/site/contact/threads/",
            {"subject": "Research collaboration", "content": "Interested in a joint project."},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["subject"], "Research collaboration")
        self.assertEqual(len(payload["messages"]), 1)
        self.assertEqual(payload["messages"][0]["content"], "Interested in a joint project.")
        self.assertEqual(ContactThread.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.count(), 1)

    @override_settings(
        RECAPTCHA_SITE_KEY="site-key",
        RECAPTCHA_SECRET_KEY="secret-key",
        RECAPTCHA_MIN_SCORE=0.7,
    )
    @patch("apps.base.controllers.verify_recaptcha_token")
    def test_contact_thread_requires_valid_recaptcha_when_enabled(self, verify_mock):
        user = get_user_model().objects.create_user(
            username="contact-user-2",
            email="contact2@example.com",
        )
        self.client.force_login(user)
        verify_mock.return_value = Mock(success=False)

        response = self.client.post(
            "/api/site/contact/threads/",
            {
                "subject": "Help",
                "content": "Need assistance.",
                "recaptcha_token": "bad-token",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactThread.objects.count(), 0)

    def test_contact_threads_lists_only_requester_threads(self):
        owner = get_user_model().objects.create_user(username="owner")
        other = get_user_model().objects.create_user(username="other")
        owner_thread = ContactThread.objects.create(requester=owner, subject="Owner thread")
        other_thread = ContactThread.objects.create(requester=other, subject="Other thread")
        ContactMessage.objects.create(thread=owner_thread, sender=owner, content="Owner message")
        ContactMessage.objects.create(thread=other_thread, sender=other, content="Other message")
        self.client.force_login(owner)

        response = self.client.get("/api/site/contact/threads/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["subject"], "Owner thread")

    @override_settings(
        RECAPTCHA_SITE_KEY="",
        RECAPTCHA_SECRET_KEY="",
    )
    def test_authenticated_user_can_reply_to_own_thread(self):
        owner = get_user_model().objects.create_user(username="thread-owner")
        thread = ContactThread.objects.create(requester=owner, subject="Existing thread")
        ContactMessage.objects.create(thread=thread, sender=owner, content="Initial")
        self.client.force_login(owner)

        response = self.client.post(
            f"/api/site/contact/threads/{thread.pk}/messages/",
            {"content": "Follow-up details"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(len(payload["messages"]), 2)
        self.assertEqual(payload["messages"][-1]["content"], "Follow-up details")

    def test_github_session_exposes_recaptcha_configuration(self):
        response = self.client.get("/api/auth/github/session/")
        self.assertIn("recaptcha_enabled", response.json())
        self.assertIn("recaptcha_site_key", response.json())


class GithubViewSetTests(TestCase):
    def setUp(self):
        cache.clear()

    def _mock_response(self, payload, ok=True):
        response = Mock()
        response.ok = ok
        response.json.return_value = payload
        return response

    def test_create_from_gist_uses_first_markdown_like_file(self):
        entry, _ = BlogEntry.create_from_gist(
            {
                "id": "gist-readme",
                "created_at": "2025-12-15T01:39:00+00:00",
                "updated_at": "2025-12-15T01:39:00+00:00",
                "description": "README gist",
                "html_url": "https://gist.github.com/etherbeing/gist-readme",
                "files": {
                    "README.md": {"filename": "README.md", "language": "Markdown", "content": "# Title"},
                    "app.py": {"filename": "app.py", "language": "Python", "content": "print('hi')"},
                },
            }
        )

        self.assertEqual(entry.content, "# Title")
        self.assertEqual(entry.image_url, "")

    def test_create_from_gist_extracts_image_png_when_present(self):
        entry, _ = BlogEntry.create_from_gist(
            {
                "id": "gist-with-image",
                "created_at": "2025-12-15T01:39:00+00:00",
                "updated_at": "2025-12-15T01:39:00+00:00",
                "description": "Image gist",
                "html_url": "https://gist.github.com/etherbeing/gist-with-image",
                "files": {
                    "content.md": {"filename": "content.md", "language": "Markdown", "content": "# Title"},
                    "image.png": {
                        "filename": "image.png",
                        "type": "image/png",
                        "raw_url": "https://gist.githubusercontent.com/image.png",
                    },
                },
            }
        )

        self.assertEqual(entry.image_url, "https://gist.githubusercontent.com/image.png")

    def test_create_from_gist_uses_first_available_image_file(self):
        entry, _ = BlogEntry.create_from_gist(
            {
                "id": "gist-with-jpg",
                "created_at": "2025-12-15T01:39:00+00:00",
                "updated_at": "2025-12-15T01:39:00+00:00",
                "description": "Image gist",
                "html_url": "https://gist.github.com/etherbeing/gist-with-jpg",
                "files": {
                    "cover.jpg": {
                        "filename": "cover.jpg",
                        "type": "image/jpeg",
                        "raw_url": "https://gist.githubusercontent.com/cover.jpg",
                    },
                    "content.md": {"filename": "content.md", "language": "Markdown", "content": "# Title"},
                },
            }
        )

        self.assertEqual(entry.image_url, "https://gist.githubusercontent.com/cover.jpg")

    def test_create_from_gist_extracts_metadata_when_present(self):
        entry, _ = BlogEntry.create_from_gist(
            {
                "id": "gist-with-metadata",
                "created_at": "2025-12-15T01:39:00+00:00",
                "updated_at": "2025-12-15T01:39:00+00:00",
                "description": "Metadata gist",
                "html_url": "https://gist.github.com/etherbeing/gist-with-metadata",
                "files": {
                    "content.md": {"filename": "content.md", "language": "Markdown", "content": "# Title"},
                    "metadata.json": {
                        "filename": "metadata.json",
                        "content": '{"category":"researches","social_networks":["telegram","discord"]}',
                    },
                },
            }
        )

        self.assertEqual(entry.category, "researches")
        self.assertEqual(entry.social_networks, ["telegram", "discord"])

    @patch("apps.base.controllers.requests.request")
    def test_list_projects_fetches_from_github(self, request_mock):
        request_mock.side_effect = [
            self._mock_response(
                [
                    {
                        "id": 123,
                        "name": "etherbeing_official",
                        "description": "Website",
                        "stargazers_count": 10,
                        "watchers_count": 6,
                        "created_at": "2025-12-15T01:39:00+00:00",
                        "updated_at": "2025-12-15T01:39:00+00:00",
                        "pushed_at": "2025-12-15T01:39:00+00:00",
                        "html_url": "https://github.com/etherbeing/etherbeing_official",
                        "language": "TypeScript",
                        "languages_url": "https://api.github.com/repos/etherbeing/etherbeing_official/languages",
                    }
                ]
            ),
            self._mock_response({"TypeScript": 1000, "Python": 250}),
        ]

        response = self.client.get("/api/projects/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["github_id"], "123")
        self.assertEqual(payload[0]["languages"], ["TypeScript", "Python"])
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(request_mock.call_count, 2)
        self.assertIn(
            "users/etherbeing/repos?type=public&sort=updated&per_page=100",
            request_mock.call_args_list[0].args[1],
        )
        self.assertIn(
            "repos/etherbeing/etherbeing_official/languages",
            request_mock.call_args_list[1].args[1],
        )

    def test_list_gists_excludes_hidden_entries(self):
        BlogEntry.objects.create(
            gist_id="visible-gist",
            description="Visible",
            content="# Visible",
            html_url="https://gist.github.com/etherbeing/visible-gist",
            hide_from_web=False,
        )
        BlogEntry.objects.create(
            gist_id="hidden-gist",
            description="Hidden",
            content="# Hidden",
            html_url="https://gist.github.com/etherbeing/hidden-gist",
            hide_from_web=True,
        )

        response = self.client.get("/api/gists/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual([entry["gist_id"] for entry in payload], ["visible-gist"])

    def test_get_gist_returns_not_found_for_hidden_entry(self):
        BlogEntry.objects.create(
            gist_id="hidden-gist",
            description="Hidden",
            content="# Hidden",
            html_url="https://gist.github.com/etherbeing/hidden-gist",
            hide_from_web=True,
        )

        response = self.client.get("/api/gist/hidden-gist/")

        self.assertEqual(response.status_code, 404)

    @patch(
        "apps.base.controllers.requests.request",
        side_effect=Exception("network should not be called"),
    )
    def test_list_projects_uses_cache(self, request_mock):
        Project.objects.create(
            github_id="999",
            name="cached-project",
            stargazers_count=1,
            watchers_count=1,
        )
        cache.set(
            "projects",
            [
                {
                    "github_id": "999",
                    "name": "cached-project",
                    "description": None,
                    "stargazers_count": 1,
                    "watchers_count": 1,
                    "created_at": None,
                    "updated_at": None,
                    "pushed_at": None,
                    "html_url": None,
                    "language": None,
                }
            ],
            timeout=60,
        )

        response = self.client.get("/api/projects/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "cached-project")

    @patch("apps.base.controllers.requests.request")
    def test_get_project_fetches_specific_project_when_missing(self, request_mock):
        request_mock.return_value = self._mock_response(
            {
                "id": 456,
                "name": "backend",
                "description": "Django API",
                "stargazers_count": 3,
                "watchers_count": 2,
                "created_at": "2025-12-15T01:39:00+00:00",
                "updated_at": "2025-12-15T01:39:00+00:00",
                "pushed_at": "2025-12-15T01:39:00+00:00",
                "html_url": "https://github.com/etherbeing/backend",
                "language": "Python",
            }
        )

        response = self.client.get("/api/project/456/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "backend")
        self.assertTrue(Project.objects.filter(github_id="456").exists())

    def test_create_from_repo_accepts_long_public_github_metadata(self):
        long_name = "very-long-public-repository-name-" * 6
        long_description = "Detailed public repository description " * 20

        project, _ = Project.create_from_repo(
            {
                "id": 789,
                "name": long_name,
                "description": long_description,
                "stargazers_count": 3,
                "watchers_count": 2,
                "created_at": "2025-12-15T01:39:00+00:00",
                "updated_at": "2025-12-15T01:39:00+00:00",
                "pushed_at": "2025-12-15T01:39:00+00:00",
                "html_url": "https://github.com/etherbeing/very-long-public-repository-name",
                "language": "Python",
            },
            {"Python": 1000, "Rust": 500, "Dockerfile": 100},
        )

        self.assertEqual(project.name, long_name)
        self.assertEqual(project.description, long_description)
        self.assertEqual(project.languages, ["Python", "Rust", "Dockerfile"])

    @patch("apps.base.controllers.requests.request")
    def test_list_gists_fetches_from_github(self, request_mock):
        request_mock.return_value = self._mock_response(
            [
                {
                    "id": "gist-123",
                    "created_at": "2025-12-15T01:39:00+00:00",
                    "updated_at": "2025-12-15T01:39:00+00:00",
                    "description": "A blog post",
                    "html_url": "https://gist.github.com/etherbeing/gist-123",
                    "files": {
                        "content.md": {"filename": "content.md", "content": "# Hello"},
                        "image.png": {
                            "filename": "image.png",
                            "raw_url": "https://gist.githubusercontent.com/cover.png",
                        },
                    },
                }
            ]
        )

        response = self.client.get("/api/gists/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["gist_id"], "gist-123")
        self.assertEqual(payload[0]["image_url"], "https://gist.githubusercontent.com/cover.png")
        self.assertTrue(BlogEntry.objects.filter(gist_id="gist-123").exists())
        request_mock.assert_called_once()
        self.assertIn("users/etherbeing/gists", request_mock.call_args.args[1])

    @patch("apps.base.controllers.requests.request")
    def test_get_gist_fetches_full_gist_when_cached_metadata_has_no_content(self, request_mock):
        BlogEntry.objects.create(
            gist_id="gist-empty",
            description="Metadata only",
            content="",
            html_url="https://gist.github.com/etherbeing/gist-empty",
        )
        request_mock.return_value = self._mock_response(
            {
                "id": "gist-empty",
                "created_at": "2025-12-15T01:39:00+00:00",
                "updated_at": "2025-12-15T01:39:00+00:00",
                "description": "Metadata only",
                "html_url": "https://gist.github.com/etherbeing/gist-empty",
                "files": {"README.md": {"filename": "README.md", "language": "Markdown", "content": "# Full content"}},
            }
        )

        response = self.client.get("/api/gist/gist-empty/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["content"], "# Full content")
        self.assertEqual(BlogEntry.objects.get(gist_id="gist-empty").content, "# Full content")

    @patch("apps.base.controllers.requests.request")
    def test_get_gist_fetches_specific_gist_when_missing(self, request_mock):
        request_mock.return_value = self._mock_response(
            {
                "id": "gist-234",
                "created_at": "2025-12-15T01:39:00+00:00",
                "updated_at": "2025-12-15T01:39:00+00:00",
                "description": "Single gist",
                "html_url": "https://gist.github.com/etherbeing/gist-234",
                "files": {"content.md": {"content": "# Entry"}},
            }
        )

        response = self.client.get("/api/gist/gist-234/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["gist_id"], "gist-234")
        self.assertEqual(BlogEntry.objects.get(gist_id="gist-234").content, "# Entry")


class AdminAuthTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_superuser(
            username="localadmin",
            email="localadmin@example.com",
            password="test-pass-123",
        )

    @override_settings(
        RECAPTCHA_SITE_KEY="",
        RECAPTCHA_SECRET_KEY="",
    )
    def test_admin_login_accepts_password_without_recaptcha_when_disabled(self):
        login_page = self.client.get("/admin/login/")
        self.assertContains(login_page, "admin-theme.css")
        self.assertContains(login_page, "admin-theme.js")
        self.assertContains(login_page, "cdn.tailwindcss.com")
        self.assertContains(login_page, "etherbeing-admin-login-page")
        self.assertContains(login_page, "Operate the platform from a fully controlled interface.")
        self.assertNotContains(login_page, "iframe")
        self.assertNotContains(login_page, "Create Initial Superuser")

        response = self.client.post(
            "/admin/login/?next=/admin/",
            {
                "username": "localadmin",
                "password": "test-pass-123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/admin/")

    def test_admin_index_uses_custom_theme_branding(self):
        self.client.force_login(self.user)

        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin-theme.css")
        self.assertContains(response, "cdn.tailwindcss.com")
        self.assertContains(response, "Control Surface")
        self.assertContains(response, "MIT License")

    def test_admin_overridden_views_render_explicit_template_wrappers(self):
        self.client.force_login(self.user)
        initialize_site_content()

        index_response = self.client.get("/admin/")
        changelist_response = self.client.get("/admin/base/service/")

        self.assertEqual(index_response.status_code, 200)
        self.assertContains(index_response, "etherbeing-admin-dashboard-main")
        self.assertContains(index_response, "etherbeing-admin-dashboard-sidebar")
        self.assertContains(index_response, "etherbeing-admin-app-list")
        self.assertContains(index_response, "Publishing control")
        self.assertContains(index_response, "Open publisher")
        self.assertContains(index_response, "GitHub publishing token")

        self.assertEqual(changelist_response.status_code, 200)
        self.assertContains(changelist_response, "etherbeing-admin-nav-shell")
        self.assertContains(changelist_response, "etherbeing-admin-change-list-main")
        self.assertContains(changelist_response, "etherbeing-admin-change-list-shell")
        self.assertContains(changelist_response, "etherbeing-admin-search-row")
        self.assertContains(changelist_response, "etherbeing-admin-object-tools")
        self.assertContains(changelist_response, "Publish post")

    def test_admin_change_form_shows_detail_panel_sidebar(self):
        self.client.force_login(self.user)
        site_content = initialize_site_content()

        response = self.client.get(f"/admin/base/sitecontent/{site_content.pk}/change/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "model-detail-panel")
        self.assertContains(response, "Detail panel")
        self.assertContains(response, "Current context")

    def test_admin_publish_post_page_renders_editor(self):
        self.client.force_login(self.user)

        response = self.client.get("/admin/publishing/blog-posts/new/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "etherbeing-rich-editor")
        self.assertContains(response, "etherbeing-rich-preview")
        self.assertContains(response, "Full screen editor")
        self.assertContains(response, "Full screen preview")
        self.assertContains(response, "Live preview")
        self.assertContains(response, "social_networks")
        self.assertContains(response, "Channel readiness")
        self.assertContains(response, "GitHub publishing token")

    @patch("apps.base.publishing.requests.post")
    def test_admin_publish_post_creates_gist_and_publication_record(self, post_mock):
        self.user.github_access_token = "test-publish-token"
        self.user.save(update_fields=["github_access_token"])
        self.client.force_login(self.user)

        def response_with(payload):
            mock = Mock()
            mock.json.return_value = payload
            mock.raise_for_status.return_value = None
            return mock

        post_mock.side_effect = [
            response_with(
                {
                    "id": "gist-published",
                    "created_at": "2026-03-13T12:00:00+00:00",
                    "updated_at": "2026-03-13T12:00:00+00:00",
                    "description": "New admin post",
                    "html_url": "https://gist.github.com/etherbeing/gist-published",
                    "files": {
                        "content.md": {"content": "<p>Hello world</p>"},
                        "metadata.json": {"content": '{"category":"cybersecurity","social_networks":["telegram","discord"]}'},
                    },
                }
            ),
            response_with({"ok": True}),
            response_with({"ok": True}),
        ]

        response = self.client.post(
            "/admin/publishing/blog-posts/new/",
            {
                "title": "New admin post",
                "excerpt": "Summary",
                "category": "cybersecurity",
                "social_networks": ["telegram", "discord"],
                "content": "<p>Hello world</p>",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(BlogEntry.objects.filter(gist_id="gist-published").exists())
        self.assertTrue(PublishedPost.objects.filter(gist_id="gist-published").exists())
        published = PublishedPost.objects.get(gist_id="gist-published")
        self.assertEqual(published.social_networks, ["telegram", "discord"])
        self.assertContains(response, "Blog post published successfully")

    @override_settings(DEBUG=True)
    def test_admin_login_shows_bootstrap_superuser_button_when_no_superuser_exists(self):
        get_user_model().objects.filter(pk=self.user.pk).delete()

        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Initial Superuser")
        self.assertContains(response, "bootstrap-superuser-modal")
        self.assertContains(response, "etherbeing-modal-backdrop")

    @override_settings(DEBUG=True)
    def test_bootstrap_superuser_creates_first_superuser(self):
        get_user_model().objects.filter(pk=self.user.pk).delete()

        response = self.client.post(
            "/admin/bootstrap-superuser/",
            {
                "username": "bootstrap-admin",
                "email": "bootstrap@example.com",
                "password1": "test-pass-123-xyz",
                "password2": "test-pass-123-xyz",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            get_user_model().objects.filter(
                username="bootstrap-admin",
                is_superuser=True,
                is_staff=True,
            ).exists()
        )
        self.assertTrue(SiteContent.objects.filter(slug="primary").exists())
        self.assertGreater(Service.objects.count(), 0)
        frontend_service = Service.objects.get(slug="frontend-web-development")
        self.assertTrue(frontend_service.headline)
        self.assertTrue(frontend_service.deliverables)
        self.assertContains(response, "Superuser created successfully")

    @override_settings(
        RECAPTCHA_SITE_KEY="site-key",
        RECAPTCHA_SECRET_KEY="secret-key",
        RECAPTCHA_MIN_SCORE=0.7,
    )
    def test_admin_login_shows_recaptcha_checkbox_when_enabled(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "g-recaptcha")
        self.assertContains(response, "https://www.google.com/recaptcha/api.js")

    @override_settings(
        RECAPTCHA_SITE_KEY="site-key",
        RECAPTCHA_SECRET_KEY="secret-key",
        RECAPTCHA_MIN_SCORE=0.7,
    )
    @patch("apps.base.forms.verify_recaptcha_token")
    def test_admin_login_rejects_low_recaptcha_score(self, verify_mock):
        verify_mock.return_value = Mock(success=False)

        response = self.client.post(
            "/admin/login/?next=/admin/",
            {
                "username": "localadmin",
                "password": "test-pass-123",
                "recaptcha_token": "token-123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "reCAPTCHA verification failed")

    @override_settings(
        RECAPTCHA_SITE_KEY="site-key",
        RECAPTCHA_SECRET_KEY="secret-key",
        RECAPTCHA_MIN_SCORE=0.7,
    )
    @patch("apps.base.forms.verify_recaptcha_token")
    def test_admin_login_accepts_high_recaptcha_score(self, verify_mock):
        verify_mock.return_value = Mock(success=True)

        response = self.client.post(
            "/admin/login/?next=/admin/",
            {
                "username": "localadmin",
                "password": "test-pass-123",
                "recaptcha_token": "token-123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/admin/")

    @override_settings(
        GITHUB_OAUTH_CLIENT_ID="github-client-id",
        GITHUB_OAUTH_CLIENT_SECRET="github-client-secret",
        GITHUB_ADMIN_USERS=["etherbeing"],
        GITHUB_SUPERUSER_USERS=["etherbeing"],
        RECAPTCHA_SITE_KEY="",
        RECAPTCHA_SECRET_KEY="",
    )
    def test_admin_github_login_redirects_with_required_scopes(self):
        response = self.client.get("/admin/github/login/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("https://github.com/login/oauth/authorize", response.headers["Location"])
        self.assertIn("scope=read%3Auser+user%3Aemail+gist+repo", response.headers["Location"])

    @override_settings(
        GITHUB_OAUTH_CLIENT_ID="github-client-id",
        GITHUB_OAUTH_CLIENT_SECRET="github-client-secret",
        GITHUB_ADMIN_USERS=["etherbeing"],
        GITHUB_SUPERUSER_USERS=["etherbeing"],
        RECAPTCHA_SITE_KEY="site-key",
        RECAPTCHA_SECRET_KEY="secret-key",
    )
    @patch("apps.base.admin.verify_recaptcha_token")
    def test_admin_github_login_requires_recaptcha_when_enabled(self, verify_mock):
        verify_mock.return_value = Mock(success=False)

        response = self.client.get("/admin/github/login/?recaptcha_token=bad-token", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], "/admin/login/")

    @override_settings(
        GITHUB_OAUTH_CLIENT_ID="github-client-id",
        GITHUB_OAUTH_CLIENT_SECRET="github-client-secret",
        GITHUB_ADMIN_USERS=["etherbeing"],
        GITHUB_SUPERUSER_USERS=["etherbeing"],
    )
    @patch("apps.base.admin_auth.fetch_github_primary_email")
    @patch("apps.base.admin_auth.fetch_github_profile")
    @patch("apps.base.admin_auth.exchange_code_for_token")
    def test_admin_github_callback_creates_staff_user_and_logs_in(
        self,
        exchange_mock,
        profile_mock,
        email_mock,
    ):
        session = self.client.session
        session["github_oauth_state"] = "state-123"
        session.save()
        exchange_mock.return_value = {
            "access_token": "access-token-123",
            "scope": "read:user,gist,repo,user:email",
        }
        profile_mock.return_value = {
            "login": "etherbeing",
            "name": "Ether Being",
            "email": "",
        }
        email_mock.return_value = "etherbeing@example.com"

        response = self.client.get("/admin/github/callback/?state=state-123&code=oauth-code")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/admin/")
        github_user = get_user_model().objects.get(username="etherbeing")
        self.assertTrue(github_user.is_staff)
        self.assertTrue(github_user.is_superuser)
        self.assertEqual(github_user.github_access_token, "access-token-123")
        self.assertEqual(github_user.github_token_scope, "read:user,gist,repo,user:email")
        self.assertEqual(int(self.client.session["_auth_user_id"]), github_user.pk)

    @override_settings(
        GITHUB_OAUTH_CLIENT_ID="github-client-id",
        GITHUB_OAUTH_CLIENT_SECRET="github-client-secret",
        GITHUB_ADMIN_USERS=["etherbeing"],
        GITHUB_SUPERUSER_USERS=["etherbeing"],
    )
    @patch("apps.base.admin_auth.fetch_github_profile")
    @patch("apps.base.admin_auth.exchange_code_for_token")
    def test_admin_github_callback_rejects_non_admin_user(
        self,
        exchange_mock,
        profile_mock,
    ):
        session = self.client.session
        session["github_oauth_state"] = "state-123"
        session.save()
        exchange_mock.return_value = {
            "access_token": "access-token-123",
            "scope": "read:user,gist,repo,user:email",
        }
        profile_mock.return_value = {
            "login": "someone-else",
            "name": "No Access",
            "email": "no-access@example.com",
        }

        response = self.client.get("/admin/github/callback/?state=state-123&code=oauth-code", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "is not allowed to access the admin")


class FrontendGithubAuthTests(TestCase):
    def setUp(self):
        cache.clear()

    @override_settings(
        GITHUB_OAUTH_CLIENT_ID="github-client-id",
        GITHUB_OAUTH_CLIENT_SECRET="github-client-secret",
    )
    def test_frontend_github_login_redirects_with_next_url(self):
        response = self.client.get("/api/auth/github/login/?next=/blog/entry/?slug=gist-123")

        self.assertEqual(response.status_code, 302)
        self.assertIn("https://github.com/login/oauth/authorize", response.headers["Location"])
        self.assertIn("scope=read%3Auser+user%3Aemail", response.headers["Location"])
        self.assertNotIn("repo", response.headers["Location"])
        session = self.client.session
        self.assertEqual(session["github_oauth_flow"]["flow"], "frontend")
        self.assertEqual(session["github_oauth_flow"]["next_url"], "/blog/entry/?slug=gist-123")

    @override_settings(
        GITHUB_OAUTH_CLIENT_ID="github-client-id",
        GITHUB_OAUTH_CLIENT_SECRET="github-client-secret",
    )
    def test_frontend_comment_login_requests_gist_scope_without_repo_scope(self):
        response = self.client.get("/api/auth/github/login/?next=/blog/entry/?slug=gist-123&intent=comment")

        self.assertEqual(response.status_code, 302)
        self.assertIn("scope=read%3Auser+user%3Aemail+gist", response.headers["Location"])
        self.assertNotIn("repo", response.headers["Location"])

    @override_settings(
        GITHUB_OAUTH_CLIENT_ID="github-client-id",
        GITHUB_OAUTH_CLIENT_SECRET="github-client-secret",
        GITHUB_ADMIN_USERS=["etherbeing"],
        GITHUB_SUPERUSER_USERS=["etherbeing"],
    )
    @patch("apps.base.admin_auth.fetch_github_primary_email")
    @patch("apps.base.admin_auth.fetch_github_profile")
    @patch("apps.base.admin_auth.exchange_code_for_token")
    def test_frontend_github_callback_logs_regular_user_and_redirects_to_next(
        self,
        exchange_mock,
        profile_mock,
        email_mock,
    ):
        session = self.client.session
        session["github_oauth_state"] = "state-frontend"
        session["github_oauth_flow"] = {
            "flow": "frontend",
            "next_url": "/blog/entry/?slug=gist-123",
        }
        session.save()
        exchange_mock.return_value = {
            "access_token": "front-access-token",
            "scope": "read:user,gist,repo,user:email",
        }
        profile_mock.return_value = {
            "login": "reader-user",
            "name": "Reader User",
            "email": "",
        }
        email_mock.return_value = "reader@example.com"

        response = self.client.get("/api/auth/github/callback/?state=state-frontend&code=oauth-code")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/blog/entry/?slug=gist-123")
        user = get_user_model().objects.get(username="reader-user")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.github_access_token, "front-access-token")

    def test_frontend_github_session_returns_anonymous_when_logged_out(self):
        response = self.client.get("/api/auth/github/session/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_authenticated"], False)
        self.assertTrue(response.json()["csrf_token"])

    def test_frontend_github_session_returns_logged_user(self):
        user = get_user_model().objects.create_user(
            username="reader-user",
            email="reader@example.com",
            github_login="reader-user",
            github_access_token="access-token",
            github_token_scope="read:user,user:email",
        )
        self.client.force_login(user)

        response = self.client.get("/api/auth/github/session/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["is_authenticated"], True)
        self.assertEqual(payload["username"], "reader-user")
        self.assertEqual(payload["github_login"], "reader-user")
        self.assertEqual(payload["can_comment_on_gists"], False)


class GithubCommentTests(TestCase):
    def setUp(self):
        cache.clear()

    def _mock_response(self, payload, ok=True):
        response = Mock()
        response.ok = ok
        response.json.return_value = payload
        response.raise_for_status.return_value = None
        return response

    def test_post_gist_comment_requires_authenticated_user(self):
        response = self.client.post(
            "/api/gist/gist-123/comments/",
            {"content": "Great post"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_post_gist_comment_requires_gist_scope(self):
        user = get_user_model().objects.create_user(
            username="reader-user",
            email="reader@example.com",
            github_login="reader-user",
            github_access_token="access-token",
            github_token_scope="read:user,user:email",
        )
        self.client.force_login(user)

        response = self.client.post(
            "/api/gist/gist-123/comments/",
            {"content": "Great post"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

    @patch("apps.base.controllers.requests.post")
    @patch("apps.base.controllers.requests.get")
    def test_post_gist_comment_uses_logged_in_users_github_token(
        self,
        get_mock,
        post_mock,
    ):
        user = get_user_model().objects.create_user(
            username="reader-user",
            email="reader@example.com",
            github_login="reader-user",
            github_access_token="access-token",
            github_token_scope="read:user,user:email,gist",
        )
        self.client.force_login(user)
        get_mock.return_value = self._mock_response(
            [
                {
                    "id": 22,
                    "user": {"login": "reader-user"},
                    "body": "Great post",
                    "created_at": "2025-12-15T01:39:00+00:00",
                }
            ]
        )
        post_mock.return_value = self._mock_response(
            {
                "id": 22,
                "user": {"login": "reader-user"},
                "body": "Great post",
                "created_at": "2025-12-15T01:39:00+00:00",
            }
        )

        response = self.client.post(
            "/api/gist/gist-123/comments/",
            {"content": "Great post"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["content"], "Great post")
        self.assertEqual(payload["username"], "reader-user")
        self.assertEqual(
            post_mock.call_args.kwargs["headers"]["Authorization"],
            "Bearer access-token",
        )
        self.assertIn("/gists/gist-123/comments", post_mock.call_args.args[0])

    @patch("apps.base.controllers.requests.get")
    def test_get_gist_comments_syncs_github_comments(self, get_mock):
        get_mock.return_value = self._mock_response(
            [
                {
                    "id": 22,
                    "user": {"login": "reader-user"},
                    "body": "Great post",
                    "created_at": "2025-12-15T01:39:00+00:00",
                }
            ]
        )

        response = self.client.get("/api/gist/gist-123/comments/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["username"], "reader-user")
        self.assertEqual(payload[0]["content"], "Great post")
