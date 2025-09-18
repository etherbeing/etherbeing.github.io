<script lang="ts">
    import { _ } from "svelte-i18n";
    import divider from "/src/assets/dark/images/divider.png"

    interface Skill {
        expertise_level: number;
        name: string;
    }
    let skills: Array<Skill> = $state([
        {
            expertise_level: 67,
            name: "Cybersecurity",
        },
        {
            expertise_level: 100,
            name: "Python",
        },
        {
            name: "Django",
            expertise_level: 100
        },
        {
            name: "ReactJS",
            expertise_level: 100
        },
        {
            name: "Svelte",
            expertise_level: 100
        },
        {
            name: "Rust",
            expertise_level: 70
        },
        {
            name: "Linux",
            expertise_level: 80
        },
        {
            name: "Networking",
            expertise_level: 60
        },
        {
            name: "DevOps",
            expertise_level: 100
        },
        {
            name: "Docker",
            expertise_level: 90
        },
        {
            name: "Jenkins",
            expertise_level: 70
        },
        {
            name: "Github Actions",
            expertise_level: 80
        },
        {
            name: "DNS",
            expertise_level: 45
        },
        {
            name: "AI",
            expertise_level: 68
        },
        {
            name: "Neural Networks",
            expertise_level: 75
        }
    ]);
</script>

<div class="unslate_co--section section-counter" id="skills-section">
    <div class="container">
        <div class="section-heading-wrap text-center mb-5">
            <h2 class="heading-h2 text-center divider">
                <span class="gsap-reveal">{$_("skills.title")}</span>
            </h2>
            <span class="gsap-reveal"
                ><img
                    src={divider}
                    alt="divider"
                    width="76"
                /></span
            >
        </div>

        <div class="row pt-5">
            {#each skills as skill, i}
                <div
                    class="col-6 col-sm-6 mb-5 mb-lg-0 col-md-6 col-lg-3 mt-3"
                    data-aos="fade-up"
                    data-aos-delay={i * 100}
                >
                    <div class="counter-v1 text-center">
                        <span class="number-wrap">
                            <span
                                class="number number-counter"
                                data-number={skill.expertise_level}>0</span
                            >
                            <span class="append-text">%</span>
                        </span>
                        <span class="counter-label">{skill.name}</span>
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>
<!-- END .counter -->
