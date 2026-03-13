from django.db import migrations


SERVICE_DEFAULTS = [
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


def populate_services(apps, schema_editor):
    SiteContent = apps.get_model("base", "SiteContent")
    Service = apps.get_model("base", "Service")

    site_content = SiteContent.objects.filter(slug="primary").first()
    if site_content is None:
        return

    for index, service_defaults in enumerate(SERVICE_DEFAULTS):
        Service.objects.update_or_create(
            site_content=site_content,
            slug=service_defaults["slug"],
            defaults={
                **service_defaults,
                "sort_order": index,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0024_skill_description_skill_headline_skill_image_url"),
    ]

    operations = [
        migrations.RunPython(populate_services, migrations.RunPython.noop),
    ]
