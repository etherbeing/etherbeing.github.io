from django.db import transaction

from .models import (
    AboutHighlight,
    Configuration,
    ContactGroup,
    ContactLink,
    Service,
    SiteContent,
    Skill,
)

DEFAULT_CONFIGURATION = {
    "slug": "primary",
    "site_name": "etherbeing",
    "short_name": "etherbeing",
    "site_description": "Cybersecurity, Rust engineering, biological neural networks, and research.",
    "favicon_url": "https://etherbeing.github.io/favicon.png",
    "theme_color": "#020617",
    "background_color": "#020617",
}


DEFAULT_SITE_CONTENT = {
    "slug": "primary",
    "site_title": "etherbeing",
    "hero_titles": [
        "Esteban Chacon",
        "Cybersecurity",
        "Rust",
        "Python",
        "Django",
        "ReactJS",
        "Reverse Engineering",
        "Pentesting",
        "Patching",
        "AstroJS",
        "Svelte",
        "Actix Web",
        "Web Development",
        "Zero Day Exploits",
        "Unity Game Engine",
        "Full stack development",
        "Docker",
        "DevOps",
        "Network Administrator",
        "System Administrator",
        "Phylosoraptor",
    ],
    "hero_summary": (
        "Offensive Security, Rust Systems, Biological Neural Networks, Python, "
        "CVE Forge."
    ),
    "hero_cta_label": "Download CV",
    "hero_cta_url": "/cv.pdf",
    "about_short_bio": (
        "I'm a cybersecurity enthusiast and Rust developer with a knack for "
        "solving complex problems."
    ),
    "buy_me_a_coffee_url": "https://paypal.me/etherbeing",
    "contact_intro": (
        "You can contact me anytime and I'll reach back to you as soon as "
        "possible. You can contact me either for a job proposal, a research "
        "cooperation idea, or a project you have in mind. All the information "
        "received by me from you is, unless you say otherwise, private and "
        "won't be released."
    ),
    "footer_copy": "All rights reserved © Esteban Chacon Martin",
    "footer_tagline": "Offensive Security & Rust Engineering",
    "strategy_business_idea": {
        "blog_integrations": [
            "Telegram",
            "Whatsapp",
            "LinkedIn",
            "Instagram",
            "Facebook",
            "Youtube",
        ],
        "content_to_publish": [
            "Cybersecurity",
            "Software Development",
            "DevOps",
            "Philosophy",
            "Politics",
            "Project Ads",
            "Artificial Intelligence",
            "Researches",
        ],
        "other_services": [
            "MCP tools for AI",
            "Pentesting and Bug Hunting",
            "Software Development",
            "OSINT",
            "DevOps and Cluster Deployment",
            "Marketing Tools",
            "Content Generation AI tools",
        ],
    },
}

DEFAULT_ABOUT_HIGHLIGHTS = [
    {
        "column": AboutHighlight.Column.LEFT,
        "title": "Values",
        "content": "Freedom, creativity, forward thinking, democracy, and innovation.",
    },
    {
        "column": AboutHighlight.Column.LEFT,
        "title": "Mission",
        "content": "Leave this world a little bit better than how I found it.",
    },
    {
        "column": AboutHighlight.Column.RIGHT,
        "title": "Personal Journey",
        "content": (
            "Built my own enterprise failed twice, moving forward with more "
            "experience than never."
        ),
    },
    {
        "column": AboutHighlight.Column.RIGHT,
        "title": "Core Strengths",
        "content": "Resilience, adaptability, and problem-solving.",
    },
]

DEFAULT_SKILLS = [
    {"name": "Cybersecurity", "image_key": "kali"},
    {"name": "Rust", "image_key": "rust"},
    {"name": "Pentesting", "image_key": "metasploit"},
    {"name": "Biological Neural Nets", "image_key": "tensorflow"},
    {"name": "Python", "image_key": "python"},
    {"name": "React TS", "image_key": "react"},
]

DEFAULT_SERVICES = [
    {
        "slug": "frontend-web-development",
        "title": "Frontend Web Development",
        "headline": "Design and build fast interfaces that feel intentional from the first pixel.",
        "starting_price": 50,
        "description": "Turn your ideas into a human made ready to use product",
        "overview": (
            "From landing pages to full product surfaces, I build responsive interfaces "
            "that are expressive, accessible, and ready to ship with real backend data."
        ),
        "skills": ["React JS/TS", "Svelte JS/TS", "Astro JS/TS", "Others"],
        "deliverables": [
            "Responsive UI implementation",
            "Reusable component architecture",
            "Backend API integration",
            "Performance and accessibility review",
        ],
        "process_steps": [
            "Clarify goals, pages, and conversion paths",
            "Shape interface architecture and states",
            "Implement polished frontend with real data",
            "Review responsiveness, performance, and handoff",
        ],
        "outcomes": [
            "Production-ready frontend",
            "Cleaner user journeys",
            "Consistent visual system",
        ],
        "engagement_cta": "Share the product idea, audience, and pages you need most.",
    },
    {
        "slug": "backend-api-development",
        "title": "Backend API Development",
        "headline": "Expose your data safely, clearly, and where the product actually needs it.",
        "starting_price": 50,
        "description": "Makes your data available where you need it",
        "overview": (
            "I design and implement backend services focused on maintainability, "
            "security, and clean integration with web, mobile, and internal tools."
        ),
        "skills": ["OWASP", "SQL", "Django", "Actix web", "Others"],
        "deliverables": [
            "REST or service API design",
            "Authentication and authorization flow",
            "Database modeling and migrations",
            "Operational documentation",
        ],
        "process_steps": [
            "Map entities, permissions, and workflows",
            "Design data model and service boundaries",
            "Implement endpoints, validation, and tests",
            "Prepare deployment and integration guidance",
        ],
        "outcomes": [
            "Stable backend foundation",
            "Safer data access patterns",
            "Faster product iteration",
        ],
        "engagement_cta": "Describe the data flows, integrations, and constraints you need solved.",
    },
    {
        "slug": "devops",
        "title": "DevOps",
        "headline": "Automate delivery, reduce friction, and keep infrastructure understandable.",
        "starting_price": 75,
        "description": "Automate and deliver, quickly quickly",
        "overview": (
            "I help teams ship faster with reliable environments, deployment automation, "
            "observability basics, and maintainable infrastructure decisions."
        ),
        "skills": ["Docker", "K8S", "S3", "Keycloak", "DFS", "Others"],
        "deliverables": [
            "Containerized service setup",
            "Deployment workflow automation",
            "Environment and secret strategy",
            "Runtime and operational guidance",
        ],
        "process_steps": [
            "Audit the current delivery flow",
            "Reduce manual steps and fragile config",
            "Automate build, release, and runtime pieces",
            "Document how the system is operated",
        ],
        "outcomes": [
            "More reliable releases",
            "Less configuration drift",
            "Lower operational overhead",
        ],
        "engagement_cta": "Tell me what is currently slowing deployments or hurting reliability.",
    },
    {
        "slug": "pentesting",
        "title": "Pentesting",
        "headline": "Pressure-test your system before attackers or production users do.",
        "starting_price": 100,
        "description": (
            "Check whether or not your system is secure for release (No payment "
            "required unless there are results)"
        ),
        "overview": (
            "I perform practical security reviews focused on exploitable issues, risky "
            "assumptions, and the fastest path to meaningful remediation."
        ),
        "skills": ["OWASP", "Zero Day Development", "Enumeration", "Audit", "Others"],
        "deliverables": [
            "Scoped security assessment",
            "Findings report with severity and impact",
            "Reproduction guidance",
            "Remediation recommendations",
        ],
        "process_steps": [
            "Define scope and rules of engagement",
            "Enumerate attack surface and assumptions",
            "Validate findings and business impact",
            "Deliver report and remediation support",
        ],
        "outcomes": [
            "Clearer risk visibility",
            "Actionable remediation worklist",
            "Higher confidence before release",
        ],
        "engagement_cta": "Share the target scope, timeline, and any compliance or disclosure constraints.",
    },
    {
        "slug": "odoo-and-erps",
        "title": "Odoo and ERPs",
        "headline": "Deploy business tooling that your team can actually use day to day.",
        "starting_price": 50,
        "description": (
            "Let's deploy and get you ready some nice tools for your business, "
            "like Odoo or any others ERPs (like Zohoo, etc...)"
        ),
        "overview": (
            "I help businesses evaluate, deploy, and tailor ERP-style systems so operations, "
            "inventory, sales, and reporting become easier to manage."
        ),
        "skills": ["DevOps", "Linux", "Databases", "Others"],
        "deliverables": [
            "ERP deployment and environment setup",
            "Core module configuration",
            "Integration planning",
            "Operational onboarding notes",
        ],
        "process_steps": [
            "Understand the workflows the business needs covered",
            "Choose and prepare the deployment model",
            "Configure modules and baseline integrations",
            "Document usage and operational next steps",
        ],
        "outcomes": [
            "Cleaner operations",
            "Better business visibility",
            "Reduced manual work",
        ],
        "engagement_cta": "Tell me what processes you want the ERP to centralize or improve.",
    },
    {
        "slug": "android-development",
        "title": "Android Development",
        "headline": "Ship mobile experiences that feel polished instead of merely portable.",
        "starting_price": 350,
        "description": (
            "Either you want some cross platform app or some native, you'll "
            "have it right away with me"
        ),
        "overview": (
            "I build Android and cross-platform mobile apps with a strong focus on product feel, "
            "runtime performance, and pragmatic architecture choices."
        ),
        "skills": ["Android", "Java", "React Native", "Unity", "Others"],
        "deliverables": [
            "Mobile app implementation",
            "API integration and state flow",
            "Device-ready testing support",
            "Release preparation guidance",
        ],
        "process_steps": [
            "Define the product flow and platform approach",
            "Implement the core experience and integrations",
            "Test critical states across devices",
            "Prepare release and iteration plan",
        ],
        "outcomes": [
            "Faster mobile launch path",
            "More reliable app behavior",
            "Cleaner future iteration surface",
        ],
        "engagement_cta": "Describe the app idea, target users, and whether you need native or cross-platform.",
    },
]

DEFAULT_CONTACT_GROUPS = [
    {
        "title": "Social Networks",
        "links": [
            {"label": "Github", "url": "https://github.com/etherbeing", "icon": "github"},
            {"label": "X(Twitter)", "url": "https://x.com/etherbeing_real", "icon": "x"},
            {"label": "Telegram", "url": "https://t.me/etherbeing", "icon": "telegram"},
            {
                "label": "Instagram",
                "url": "https://www.instagram.com/real_etherbeing/",
                "icon": "instagram",
            },
            {
                "label": "Reddit",
                "url": "https://www.reddit.com/user/real_etherbeing/",
                "icon": "reddit",
            },
            {"label": "Email", "url": "mailto:etherbeing99@proton.me", "icon": "email"},
        ],
    },
    {
        "title": "Cybersecurity Profiles",
        "links": [
            {
                "label": "HackerOne",
                "url": "https://hackerone.com/real_etherbeing?type=user",
                "icon": "hackerone",
            },
            {
                "label": "Bugcrowd",
                "url": "https://bugcrowd.com/h/etherbeing99",
                "icon": "bugcrowd",
            },
            {
                "label": "TryHackMe",
                "url": "https://tryhackme.com/p/etherbeing",
                "icon": "tryhackme",
            },
        ],
    },
    {
        "title": "Communities",
        "links": [
            {
                "label": "Telegram Community",
                "url": "https://t.me/etherbeing_community",
                "icon": "telegram",
            },
            {
                "label": "Discord Community",
                "url": "https://discord.gg/rP66FwWTP",
                "icon": "discord",
            },
        ],
    },
]


def initialize_configuration() -> Configuration:
    configuration, _ = Configuration.objects.update_or_create(
        slug=DEFAULT_CONFIGURATION["slug"],
        defaults={key: value for key, value in DEFAULT_CONFIGURATION.items() if key != "slug"},
    )
    return configuration


@transaction.atomic
def initialize_site_content() -> SiteContent:
    initialize_configuration()
    site_content, _ = SiteContent.objects.update_or_create(
        slug=DEFAULT_SITE_CONTENT["slug"],
        defaults={key: value for key, value in DEFAULT_SITE_CONTENT.items() if key != "slug"},
    )

    site_content.about_highlights.all().delete()
    site_content.skills.all().delete()
    site_content.services.all().delete()
    site_content.contact_groups.all().delete()

    AboutHighlight.objects.bulk_create(
        [
            AboutHighlight(site_content=site_content, sort_order=index, **highlight)
            for index, highlight in enumerate(DEFAULT_ABOUT_HIGHLIGHTS)
        ]
    )
    Skill.objects.bulk_create(
        [
            Skill(site_content=site_content, sort_order=index, **skill)
            for index, skill in enumerate(DEFAULT_SKILLS)
        ]
    )
    Service.objects.bulk_create(
        [
            Service(site_content=site_content, sort_order=index, **service)
            for index, service in enumerate(DEFAULT_SERVICES)
        ]
    )

    for group_index, group_data in enumerate(DEFAULT_CONTACT_GROUPS):
        group = ContactGroup.objects.create(
            site_content=site_content,
            title=group_data["title"],
            sort_order=group_index,
        )
        ContactLink.objects.bulk_create(
            [
                ContactLink(group=group, sort_order=link_index, **link)
                for link_index, link in enumerate(group_data["links"])
            ]
        )

    return site_content
