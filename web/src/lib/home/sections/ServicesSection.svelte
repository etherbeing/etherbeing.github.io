<script lang="ts">
    import { _ } from "svelte-i18n";

    interface Service {
        icon_src: string;
        title: string;
        description: string;
    }
    let services: Array<Service> = $state([
        {
            icon_src: "/src/assets/dark/images/svg/001-options.svg",
            title: "DevOps",
            description: `Automate your pipeline and increase delivery times by tenfolds, pay once and keep it on.`,
        },
        {
            icon_src: "/src/assets/dark/images/svg/002-chat.svg",
            title: "Artificial Intelligence",
            description: "Deploy, train and use your own models with my services, this include but is not limited to NLP models, I also include other kind of algorithms as well."
        },
        {
            icon_src: "/src/assets/dark/images/svg/003-contact-book.svg",
            title: "Team Management",
            description: "Manager your team with a good software designer, scrum manager and system architect all in one."
        },
        {
            icon_src: "/src/assets/dark/images/svg/004-percentage.svg",
            title: "Web development",
            description: "Full stack development with ultra optimized and secure endpoints, don't worry anymore about your system and instead focus in what matters most"
        },
        {
            icon_src: "/src/assets/dark/images/svg/006-goal.svg",
            title: "Cybersecurity",
            description: "Tailored pentesting with custom developed tools just for your use cases, bug hunting and more."
        },
        {
            icon_src: "/src/assets/dark/images/svg/005-line-chart.svg",
            title: "Mobile Applications",
            description: "Android and IOS dev by leveraging frameworks that are also cross compatible with PC and Linux.",
        }
    ]);
</script>

<div class="unslate_co--section" id="services-section">
    <div class="container">
        <div class="section-heading-wrap text-center mb-5">
            <h2 class="heading-h2 text-center divider">
                <span class="gsap-reveal">{$_("services.title")}</span>
            </h2>
            <span class="gsap-reveal"
                ><img
                    src="/src/assets/dark/images/divider.png"
                    alt="divider"
                    width="76"
                /></span
            >
        </div>

        <div class="row gutter-v3">
            {#each services as service, i}
                <div class="col-md-6 col-lg-4 mb-4">
                    <div
                        class="feature-v1"
                        data-aos="fade-up"
                        data-aos-delay={i * 100}
                    >
                        <div class="wrap-icon mb-3">
                            <img
                                src={service.icon_src}
                                width="45"
                                alt={service.title}
                            />
                        </div>
                        <h3>{service.title}</h3>
                        <p>{service.description}</p>
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>
