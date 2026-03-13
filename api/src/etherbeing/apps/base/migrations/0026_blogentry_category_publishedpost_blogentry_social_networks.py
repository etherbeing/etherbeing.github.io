from django.db import migrations, models
import django.db.models.deletion


EXTRA_SERVICES = [
    {
        "slug": "mcp-tools-for-ai",
        "title": "MCP Tools for AI",
        "headline": "Create agent-ready tools that make AI systems useful in real environments.",
        "starting_price": 90,
        "description": "Custom MCP-compatible tools and integrations for AI workflows.",
        "overview": "I design tool interfaces, backend capabilities, and integration surfaces that let AI agents work safely against real services, files, and domain-specific operations.",
        "skills": ["MCP", "Python", "APIs", "Tooling", "AI"],
        "deliverables": ["MCP server/tool design", "Capability implementation", "Authentication and safety constraints", "Usage documentation for agent integration"],
        "process_steps": ["Define the operations the agent should perform", "Model safe tool inputs and outputs", "Implement the MCP server and integrations", "Document and validate the agent workflow"],
        "outcomes": ["More useful AI automations", "Safer agent access patterns", "Reusable AI tooling foundation"],
        "engagement_cta": "Describe the AI workflow and the external systems the tools need to reach.",
    },
    {
        "slug": "pentesting-and-bug-hunting",
        "title": "Pentesting and Bug Hunting",
        "headline": "Find real vulnerabilities with exploit-driven thinking and reproducible evidence.",
        "starting_price": 120,
        "description": "Security testing and bug hunting focused on actionable findings.",
        "overview": "This service extends standard pentesting into bug-hunting style exploration with a focus on uncovering impactful vulnerabilities and validating exploitability.",
        "skills": ["Bug Bounty", "OWASP", "Exploitation", "Reporting", "OSINT"],
        "deliverables": ["Validated vulnerability findings", "Impact-focused technical report", "Reproduction and remediation notes", "Follow-up clarification support"],
        "process_steps": ["Scope targets and success criteria", "Enumerate and test attack surface deeply", "Validate impact and reproducibility", "Deliver prioritized findings"],
        "outcomes": ["Higher confidence in exposed surfaces", "Actionable security backlog", "Clearer risk communication"],
        "engagement_cta": "Share the program scope, application targets, and disclosure constraints.",
    },
    {
        "slug": "software-development-custom",
        "title": "Software Development",
        "headline": "Build custom software systems around the exact workflows your team needs.",
        "starting_price": 80,
        "description": "Tailored software development for product, internal tools, and automation.",
        "overview": "From greenfield apps to internal business tooling, I deliver software aligned with practical requirements, maintainability, and long-term iteration.",
        "skills": ["Python", "Rust", "Django", "React", "Architecture"],
        "deliverables": ["Functional product or internal tool", "Backend and frontend implementation", "Deployment-ready setup", "Technical documentation"],
        "process_steps": ["Clarify workflows and product requirements", "Design architecture and delivery slices", "Implement and validate features", "Prepare deployment and handoff"],
        "outcomes": ["Faster operational throughput", "Better product fit", "Cleaner software foundations"],
        "engagement_cta": "Tell me what software gap or business workflow you want to solve first.",
    },
    {
        "slug": "osint",
        "title": "OSINT",
        "headline": "Turn public information into structured intelligence for investigations and decisions.",
        "starting_price": 95,
        "description": "Open-source intelligence research and investigation support.",
        "overview": "I perform structured OSINT investigations across public sources to support security research, due diligence, attribution, and contextual intelligence work.",
        "skills": ["OSINT", "Research", "Attribution", "Correlation", "Reporting"],
        "deliverables": ["Investigation brief", "Source-backed findings", "Entity and relationship mapping", "Research summary and next steps"],
        "process_steps": ["Define the subject and intelligence goals", "Collect and correlate public evidence", "Validate confidence and context", "Deliver findings in a usable format"],
        "outcomes": ["Clearer situational awareness", "Faster investigative progress", "Reusable intelligence artifacts"],
        "engagement_cta": "Describe the research target and the questions you need answered.",
    },
    {
        "slug": "devops-and-cluster-deployment",
        "title": "DevOps and Cluster Deployment",
        "headline": "Stand up clustered environments that are actually operable after launch.",
        "starting_price": 140,
        "description": "Cluster deployment, automation, and platform operations support.",
        "overview": "I help teams deploy distributed workloads, container platforms, and clustered services with a focus on repeatability, visibility, and operator sanity.",
        "skills": ["Kubernetes", "Docker", "Observability", "IaC", "Linux"],
        "deliverables": ["Cluster deployment plan", "Environment automation", "Baseline observability and runtime guidance", "Operational runbooks"],
        "process_steps": ["Review workload and runtime requirements", "Design cluster layout and automation", "Deploy and validate platform components", "Document operations and recovery paths"],
        "outcomes": ["More resilient runtime environments", "Cleaner scaling path", "Lower operational friction"],
        "engagement_cta": "Share the workloads, scale expectations, and current deployment blockers.",
    },
    {
        "slug": "marketing-tools",
        "title": "Marketing Tools",
        "headline": "Build lean tooling that helps teams publish, measure, and iterate faster.",
        "starting_price": 75,
        "description": "Custom marketing support tools and lightweight automations.",
        "overview": "I create tools for campaign operations, content pipelines, lead capture, and reporting so marketing work becomes more structured and less manual.",
        "skills": ["Automation", "Dashboards", "Content Pipelines", "Integrations", "Analytics"],
        "deliverables": ["Custom workflow or dashboard tooling", "3rd-party integration setup", "Data collection and reporting flow", "Operational documentation"],
        "process_steps": ["Map the marketing workflow bottlenecks", "Design the smallest high-value tool surface", "Implement integrations and reporting logic", "Document and iterate with operators"],
        "outcomes": ["Less manual coordination", "Better visibility into campaigns", "Faster publishing operations"],
        "engagement_cta": "Describe the campaign or content workflow that currently feels too manual.",
    },
    {
        "slug": "content-generation-ai-tools",
        "title": "Content Generation AI Tools",
        "headline": "Create AI-assisted content systems without losing editorial control.",
        "starting_price": 85,
        "description": "AI-powered tooling for content drafting, categorization, and publishing flows.",
        "overview": "I build AI-assisted content systems that support drafting, tagging, workflow routing, and publishing operations while keeping humans in control of the final output.",
        "skills": ["LLMs", "Prompting", "Content Ops", "Automation", "Integrations"],
        "deliverables": ["Content generation workflow tooling", "Prompt and template setup", "Publishing or review integration", "Operator-facing controls and documentation"],
        "process_steps": ["Define the content workflow and review boundaries", "Shape prompts, templates, and tool inputs", "Implement generation and approval surfaces", "Tune for operator feedback and consistency"],
        "outcomes": ["Faster editorial throughput", "More structured publishing flows", "Reusable AI-assisted content operations"],
        "engagement_cta": "Tell me what content pipeline you want AI to accelerate without making it chaotic.",
    },
]


def seed_extra_services(apps, schema_editor):
    SiteContent = apps.get_model("base", "SiteContent")
    Service = apps.get_model("base", "Service")
    site_content = SiteContent.objects.filter(slug="primary").first()
    if site_content is None:
        return

    starting_order = Service.objects.filter(site_content=site_content).count()
    for index, service in enumerate(EXTRA_SERVICES, start=starting_order):
        Service.objects.update_or_create(
            slug=service["slug"],
            defaults={
                **service,
                "site_content": site_content,
                "sort_order": index,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0025_populate_services_from_frontend_defaults"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogentry",
            name="category",
            field=models.CharField(
                choices=[
                    ("cybersecurity", "Cybersecurity"),
                    ("software-development", "Software Development"),
                    ("devops", "DevOps"),
                    ("philosophy", "Philosophy"),
                    ("politics", "Politics"),
                    ("project-ads", "Project Ads"),
                    ("artificial-intelligence", "Artificial Intelligence"),
                    ("researches", "Researches"),
                ],
                default="software-development",
                max_length=64,
            ),
        ),
        migrations.AddField(
            model_name="blogentry",
            name="social_networks",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.CreateModel(
            name="PublishedPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("category", models.CharField(choices=[
                    ("cybersecurity", "Cybersecurity"),
                    ("software-development", "Software Development"),
                    ("devops", "DevOps"),
                    ("philosophy", "Philosophy"),
                    ("politics", "Politics"),
                    ("project-ads", "Project Ads"),
                    ("artificial-intelligence", "Artificial Intelligence"),
                    ("researches", "Researches"),
                ], max_length=64)),
                ("social_networks", models.JSONField(blank=True, default=list)),
                ("gist_id", models.CharField(blank=True, default="", max_length=255)),
                ("gist_url", models.URLField(blank=True, default="")),
                ("content", models.TextField(default="")),
                ("excerpt", models.TextField(blank=True, default="")),
                ("notification_results", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="published_posts", to="base.user")),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.RunPython(seed_extra_services, migrations.RunPython.noop),
    ]
