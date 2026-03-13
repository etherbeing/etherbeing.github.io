from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0021_user_github_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Configuration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(default="primary", unique=True)),
                ("site_name", models.CharField(default="etherbeing", max_length=255)),
                ("short_name", models.CharField(default="etherbeing", max_length=64)),
                (
                    "site_description",
                    models.TextField(default="Cybersecurity, Rust engineering, and research."),
                ),
                (
                    "favicon_url",
                    models.URLField(blank=True, default="https://etherbeing.github.io/favicon.png"),
                ),
                ("theme_color", models.CharField(default="#020617", max_length=20)),
                ("background_color", models.CharField(default="#020617", max_length=20)),
            ],
        ),
    ]
