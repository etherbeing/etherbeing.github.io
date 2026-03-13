from django.db import transaction

from .models import (
    AboutHighlight,
    Configuration,
    ContactGroup,
    ContactLink,
    GalleryPhoto,
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
    "featured_chart_symbol": "BITSTAMP:ETHUSD",
    "featured_chart_title": "Ethereum / USD",
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
    {
        "name": "Cybersecurity",
        "image_key": "kali",
        "image_url": "/skills/kali.png",
        "headline": "Offensive validation and defensive hardening",
        "description": "Practical security work spanning pentesting, audit, enumeration, and remediation support.",
    },
    {
        "name": "Rust",
        "image_key": "rust",
        "image_url": "/skills/rust.png",
        "headline": "Systems work with reliability in mind",
        "description": "High-confidence backend and systems development with an emphasis on correctness and performance.",
    },
    {
        "name": "Pentesting",
        "image_key": "metasploit",
        "image_url": "/skills/metasploit.png",
        "headline": "Exploit thinking for real-world release readiness",
        "description": "Attack-surface review and exploit-driven testing to expose meaningful security weaknesses before launch.",
    },
    {
        "name": "Biological Neural Nets",
        "image_key": "tensorflow",
        "image_url": "/skills/tensorflow.png",
        "headline": "Research-oriented intelligence systems",
        "description": "Applied AI exploration informed by research, experimentation, and practical implementation constraints.",
    },
    {
        "name": "Python",
        "image_key": "python",
        "image_url": "/skills/python.svg",
        "headline": "Fast iteration for APIs, tooling, and automation",
        "description": "Backend services, scripting, and automation pipelines that reduce friction and move quickly.",
    },
    {
        "name": "React TS",
        "image_key": "react",
        "image_url": "/skills/react.svg",
        "headline": "Polished interactive product surfaces",
        "description": "Frontend systems with intentional UI structure, live data integration, and maintainable component design.",
    },
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
    {
        "slug": "mcp-tools-for-ai",
        "title": "MCP Tools for AI",
        "headline": "Create agent-ready tools that make AI systems useful in real environments.",
        "starting_price": 90,
        "description": "Custom MCP-compatible tools and integrations for AI workflows.",
        "overview": (
            "I design tool interfaces, backend capabilities, and integration surfaces that let AI "
            "agents work safely against real services, files, and domain-specific operations."
        ),
        "skills": ["MCP", "Python", "APIs", "Tooling", "AI"],
        "deliverables": [
            "MCP server/tool design",
            "Capability implementation",
            "Authentication and safety constraints",
            "Usage documentation for agent integration",
        ],
        "process_steps": [
            "Define the operations the agent should perform",
            "Model safe tool inputs and outputs",
            "Implement the MCP server and integrations",
            "Document and validate the agent workflow",
        ],
        "outcomes": [
            "More useful AI automations",
            "Safer agent access patterns",
            "Reusable AI tooling foundation",
        ],
        "engagement_cta": "Describe the AI workflow and the external systems the tools need to reach.",
    },
    {
        "slug": "pentesting-and-bug-hunting",
        "title": "Pentesting and Bug Hunting",
        "headline": "Find real vulnerabilities with exploit-driven thinking and reproducible evidence.",
        "starting_price": 120,
        "description": "Security testing and bug hunting focused on actionable findings.",
        "overview": (
            "This service extends standard pentesting into bug-hunting style exploration with a focus "
            "on uncovering impactful vulnerabilities and validating exploitability."
        ),
        "skills": ["Bug Bounty", "OWASP", "Exploitation", "Reporting", "OSINT"],
        "deliverables": [
            "Validated vulnerability findings",
            "Impact-focused technical report",
            "Reproduction and remediation notes",
            "Follow-up clarification support",
        ],
        "process_steps": [
            "Scope targets and success criteria",
            "Enumerate and test attack surface deeply",
            "Validate impact and reproducibility",
            "Deliver prioritized findings",
        ],
        "outcomes": [
            "Higher confidence in exposed surfaces",
            "Actionable security backlog",
            "Clearer risk communication",
        ],
        "engagement_cta": "Share the program scope, application targets, and disclosure constraints.",
    },
    {
        "slug": "software-development-custom",
        "title": "Software Development",
        "headline": "Build custom software systems around the exact workflows your team needs.",
        "starting_price": 80,
        "description": "Tailored software development for product, internal tools, and automation.",
        "overview": (
            "From greenfield apps to internal business tooling, I deliver software aligned with "
            "practical requirements, maintainability, and long-term iteration."
        ),
        "skills": ["Python", "Rust", "Django", "React", "Architecture"],
        "deliverables": [
            "Functional product or internal tool",
            "Backend and frontend implementation",
            "Deployment-ready setup",
            "Technical documentation",
        ],
        "process_steps": [
            "Clarify workflows and product requirements",
            "Design architecture and delivery slices",
            "Implement and validate features",
            "Prepare deployment and handoff",
        ],
        "outcomes": [
            "Faster operational throughput",
            "Better product fit",
            "Cleaner software foundations",
        ],
        "engagement_cta": "Tell me what software gap or business workflow you want to solve first.",
    },
    {
        "slug": "osint",
        "title": "OSINT",
        "headline": "Turn public information into structured intelligence for investigations and decisions.",
        "starting_price": 95,
        "description": "Open-source intelligence research and investigation support.",
        "overview": (
            "I perform structured OSINT investigations across public sources to support "
            "security research, due diligence, attribution, and contextual intelligence work."
        ),
        "skills": ["OSINT", "Research", "Attribution", "Correlation", "Reporting"],
        "deliverables": [
            "Investigation brief",
            "Source-backed findings",
            "Entity and relationship mapping",
            "Research summary and next steps",
        ],
        "process_steps": [
            "Define the subject and intelligence goals",
            "Collect and correlate public evidence",
            "Validate confidence and context",
            "Deliver findings in a usable format",
        ],
        "outcomes": [
            "Clearer situational awareness",
            "Faster investigative progress",
            "Reusable intelligence artifacts",
        ],
        "engagement_cta": "Describe the research target and the questions you need answered.",
    },
    {
        "slug": "devops-and-cluster-deployment",
        "title": "DevOps and Cluster Deployment",
        "headline": "Stand up clustered environments that are actually operable after launch.",
        "starting_price": 140,
        "description": "Cluster deployment, automation, and platform operations support.",
        "overview": (
            "I help teams deploy distributed workloads, container platforms, and clustered services "
            "with a focus on repeatability, visibility, and operator sanity."
        ),
        "skills": ["Kubernetes", "Docker", "Observability", "IaC", "Linux"],
        "deliverables": [
            "Cluster deployment plan",
            "Environment automation",
            "Baseline observability and runtime guidance",
            "Operational runbooks",
        ],
        "process_steps": [
            "Review workload and runtime requirements",
            "Design cluster layout and automation",
            "Deploy and validate platform components",
            "Document operations and recovery paths",
        ],
        "outcomes": [
            "More resilient runtime environments",
            "Cleaner scaling path",
            "Lower operational friction",
        ],
        "engagement_cta": "Share the workloads, scale expectations, and current deployment blockers.",
    },
    {
        "slug": "marketing-tools",
        "title": "Marketing Tools",
        "headline": "Build lean tooling that helps teams publish, measure, and iterate faster.",
        "starting_price": 75,
        "description": "Custom marketing support tools and lightweight automations.",
        "overview": (
            "I create tools for campaign operations, content pipelines, lead capture, and reporting "
            "so marketing work becomes more structured and less manual."
        ),
        "skills": ["Automation", "Dashboards", "Content Pipelines", "Integrations", "Analytics"],
        "deliverables": [
            "Custom workflow or dashboard tooling",
            "3rd-party integration setup",
            "Data collection and reporting flow",
            "Operational documentation",
        ],
        "process_steps": [
            "Map the marketing workflow bottlenecks",
            "Design the smallest high-value tool surface",
            "Implement integrations and reporting logic",
            "Document and iterate with operators",
        ],
        "outcomes": [
            "Less manual coordination",
            "Better visibility into campaigns",
            "Faster publishing operations",
        ],
        "engagement_cta": "Describe the campaign or content workflow that currently feels too manual.",
    },
    {
        "slug": "content-generation-ai-tools",
        "title": "Content Generation AI Tools",
        "headline": "Create AI-assisted content systems without losing editorial control.",
        "starting_price": 85,
        "description": "AI-powered tooling for content drafting, categorization, and publishing flows.",
        "overview": (
            "I build AI-assisted content systems that support drafting, tagging, workflow routing, "
            "and publishing operations while keeping humans in control of the final output."
        ),
        "skills": ["LLMs", "Prompting", "Content Ops", "Automation", "Integrations"],
        "deliverables": [
            "Content generation workflow tooling",
            "Prompt and template setup",
            "Publishing or review integration",
            "Operator-facing controls and documentation",
        ],
        "process_steps": [
            "Define the content workflow and review boundaries",
            "Shape prompts, templates, and tool inputs",
            "Implement generation and approval surfaces",
            "Tune for operator feedback and consistency",
        ],
        "outcomes": [
            "Faster editorial throughput",
            "More structured publishing flows",
            "Reusable AI-assisted content operations",
        ],
        "engagement_cta": "Tell me what content pipeline you want AI to accelerate without making it chaotic.",
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
            {
                "label": "TradingView",
                "url": "https://www.tradingview.com/u/etherbeing/",
                "icon": "tradingview",
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

DEFAULT_GALLERY_PHOTOS = [
    {
        "title": "Etherbeing portrait",
        "image_url": "/gallery/esteban-chacon.jpg",
        "caption": "A first gallery frame from my personal collection, ready for expansion directly from the backend admin.",
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
    site_content.gallery_photos.all().delete()

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

    GalleryPhoto.objects.bulk_create(
        [
            GalleryPhoto(site_content=site_content, sort_order=index, **photo)
            for index, photo in enumerate(DEFAULT_GALLERY_PHOTOS)
        ]
    )

    return site_content
