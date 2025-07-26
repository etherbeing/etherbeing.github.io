<script lang="ts">
    import { getContext, onMount } from "svelte";
    import type { Writable } from "svelte/store";

    const theme: Writable<"light" | "dark"> = getContext("theme");
    let headerRef: HTMLDivElement | undefined = $state();

    const generateHeader = () => {
        if (headerRef) {
            // below is done that way so we avoid the problem that has the gsap-reveal-hero that creates infinite number of nested child one reactive load
            headerRef.innerHTML = `
                    <h1 class="heading gsap-reveal-hero">Etherbeing</h1>
                    <h2 class="subheading gsap-reveal-hero">
                        I’m Esteban Chacon Martin a cybersecurity specialist
                    </h2>
                `;
        }
    };
    onMount(() => {
        theme.subscribe(generateHeader);
    });

    const BANNER_REFRESH_DELTA = 60 * 1000; // this is in milliseconds
    const BANNER_TYPE_STORAGE_KEY = "banner_type";

    enum Banner {
        NORMAL,
        VIDEO,
        SLIDER,
    }
    interface BannerType {
        banner_type: Banner;
        last_updated: Date;
    }

    let banner_type = $state(Banner.NORMAL);

    function genNewBannerType() {
        let bt_stored: BannerType = {
            banner_type: Math.floor(Math.random() * 3),
            last_updated: new Date(),
        };
        localStorage.setItem(
            BANNER_TYPE_STORAGE_KEY,
            JSON.stringify(bt_stored),
        );
        banner_type = bt_stored.banner_type;
    }
    onMount(() => {
        const raw_bt_stored = localStorage.getItem(BANNER_TYPE_STORAGE_KEY);
        if (raw_bt_stored) {
            let bt_stored: BannerType = JSON.parse(raw_bt_stored);
            bt_stored.last_updated = new Date(bt_stored.last_updated);

            console.log(
                "Obtained from storage %s and parsed into %s",
                raw_bt_stored,
                JSON.stringify(bt_stored),
            );
            if (
                Date.now() - bt_stored.last_updated.getTime() >
                BANNER_REFRESH_DELTA
            ) {
                genNewBannerType();
            } else {
                banner_type = bt_stored.banner_type;
            }
        } else {
            genNewBannerType();
        }
    });
</script>

{#if Banner.NORMAL === banner_type}
    <div
        class="cover-v1 jarallax"
        style={`background-image: url('/src/assets/${$theme}/images/cover_bg_1.jpg');`}
        id="home-section"
    >
        <div class="container">
            <div class="row align-items-center">
                <div
                    bind:this={headerRef}
                    class="col-md-7 mx-auto text-center"
                ></div>
            </div>
        </div>

        <a href="#portfolio-section" class="mouse-wrap smoothscroll">
            <span class="mouse">
                <span class="scroll"></span>
            </span>
            <span class="mouse-label">Scroll</span>
        </a>
    </div>
{:else if Banner.VIDEO === banner_type}
    <div class="cover-v1 overlay jarallax-video" id="home-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-7 mx-auto text-center">
                    <h1 class="heading gsap-reveal-hero text-white">Unfold</h1>
                    <h2 class="subheading gsap-reveal-hero text-white">
                        I’m Eric Woodman A Product Designer Based In San
                        Francisco
                    </h2>
                </div>
            </div>
        </div>

        <!-- dov -->
        <a href="#portfolio-section" class="mouse-wrap smoothscroll">
            <span class="mouse">
                <span class="scroll"></span>
            </span>
            <span class="mouse-label">Scroll</span>
        </a>
    </div>
{:else if Banner.SLIDER === banner_type}
    <div class="hero-slider-wrap">
        <div class="owl-carousel single-slider mb-0">
            <div
                class="cover-v1 jarallax"
                style={`background-image: url('/src/assets/${$theme}/images/work_1_md.jpg');`}
                id="home-section"
            >
                <div class="container">
                    <div class="row align-items-center">
                        <div class="col-md-7 mx-auto text-center">
                            <h1 class="heading gsap-reveal-hero">Unfold</h1>
                            <h2 class="subheading mb-4 gsap-reveal-hero">
                                I’m Thea Hoyer A Product Designer Based In San
                                Francisco
                            </h2>
                            <p class="gsap-reveal-hero">
                                <a
                                    href="#"
                                    class="btn btn-outline-pill btn-bg-white--hover btn-custom-light"
                                    >Download my CV</a
                                >
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <!-- END .cover-v1 -->

            <div
                class="cover-v1 jarallax"
                style={`background-image: url('/src/assets/${$theme}/images/work_2_b_full.jpg');`}
            >
                <div class="container">
                    <div class="row align-items-center">
                        <div class="col-md-12 mx-auto text-center">
                            <h1 class="heading gsap-reveal-hero">
                                One Page Portfolio
                            </h1>
                        </div>
                    </div>
                </div>
            </div>
            <!-- END .cover-v1 -->
        </div>
        <!-- END owl-carousel -->
    </div>
{/if}
<!-- END .cover-v1 -->
