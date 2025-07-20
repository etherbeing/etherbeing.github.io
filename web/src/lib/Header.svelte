<script lang="ts">
    import { getContext } from "svelte";
    import { link, location, push } from "svelte-spa-router";
    import type { Writable } from "svelte/store";

    const theme: Writable<"light" | "dark"> = getContext("theme");

    const toggleTheme = () => {
        theme.set($theme === "light" ? "dark" : "light");
    };

    const navigate = (ev: Event, to: string='/') => {
        if($location !== to){
            push(to);
        }
    };
</script>

<nav class="unslate_co--site-nav site-nav-target">
    <div class="container">
        <div class="row align-items-center justify-content-between text-left">
            <div class="col-md-5 text-right">
                <ul
                    class="site-nav-ul js-clone-nav text-left d-none d-lg-inline-block"
                >
                    <li class="has-children">
                        <a href="#home-section" onclick={navigate} class="nav-link">Home</a>
                        <ul class="dropdown">
                            <li>
                                <a href="index.html">Hero Image BG</a>
                            </li>
                            <li>
                                <a href="index-video.html">Video BG</a>
                            </li>
                            <li>
                                <a href="index-hero-slider.html">Hero Slider</a>
                            </li>
                            <li>
                                <a href="index-sidebar-menu.html"
                                    >Sidebar Menu</a
                                >
                            </li>
                            <li>
                                <a href="index-right-menu.html">Right Menu</a>
                            </li>
                        </ul>
                    </li>
                    <li>
                        <a href="#portfolio-section" onclick={navigate} class="nav-link"
                            >Portfolio</a
                        >
                    </li>
                    <li>
                        <a href="#about-section" onclick={navigate} class="nav-link">About</a>
                    </li>
                    <li>
                        <a href="#services-section" onclick={navigate} class="nav-link">Services</a
                        >
                    </li>
                </ul>
            </div>
            <div class="site-logo pos-absolute">
                <a href="/" use:link class="unslate_co--site-logo"
                    >etherbeing<span>.</span></a
                >
            </div>
            <div class="col-md-5 text-right text-lg-left">
                <ul
                    class="site-nav-ul js-clone-nav text-left d-none d-lg-inline-block"
                >
                    <li>
                        <a href="#skills-section" onclick={navigate} class="nav-link">Skills</a>
                    </li>
                    <li>
                        <a href="#testimonial-section" onclick={navigate} class="nav-link"
                            >Testimonial</a
                        >
                    </li>
                    <li>
                        <a href="#journal-section" onclick={navigate} class="nav-link">Journal</a>
                    </li>
                    <li>
                        <a
                            href="#contact-section"
                            onclick={navigate}
                            class="nav-link">Contact</a
                        >
                    </li>
                    <li>
                        <button onclick={toggleTheme}> Theme </button>
                    </li>
                </ul>

                <ul
                    class="site-nav-ul-none-onepage text-right d-inline-block d-lg-none"
                >
                    <li>
                        <a href="#" class="js-menu-toggle">Menu</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</nav>
