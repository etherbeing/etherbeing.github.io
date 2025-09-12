<script lang="ts">
    import { Moon, Sun } from "@lucide/svelte";
    import { getContext } from "svelte";
    import { link, location, push } from "svelte-spa-router";
    import type { Writable } from "svelte/store";
    import { NavLink } from "sveltestrap";
    import Dropdown from "./Dropdown.svelte";
    import { Es, Gb } from "svelte-flag-icons";

    const theme: Writable<"light" | "dark"> = getContext("theme");

    const toggleTheme = () => {
        theme.set($theme === "light" ? "dark" : "light");
    };

    const navigate = (ev: Event, to: string = "/") => {
        if ($location !== to) {
            push(to);
        }
    };
    function siteMenuClone() {
        setTimeout(() => {
            const mobile = document.querySelector(".site-mobile-inner");
            document
                .querySelectorAll(".js-clone-nav")
                .forEach((element: Element) => {
                    const newNode = element.cloneNode(true) as HTMLUListElement;
                    mobile?.appendChild(newNode);
                    newNode.className = "site-nav-wrap";
                });

            var counter = 0;
            document
                .querySelectorAll(".unslate_co--site-mobile-menu .has-children")
                .forEach(function (element) {
                    element.prepend('<span class="arrow-collapse collapsed">');

                    element
                        .querySelectorAll(".arrow-collapse")
                        .forEach((el) => {
                            (el as HTMLElement).setAttribute(
                                "data-toggle",
                                "collapse",
                            );
                            (el as HTMLElement).setAttribute(
                                "data-target",
                                "#collapseItem" + counter,
                            );
                        });

                    element.querySelectorAll("> ul").forEach((el) => {
                        el.className = "collapse";
                        el.id = "collapseItem" + counter;
                    });

                    counter++;
                });
        }, 1000);
        document.body.querySelectorAll(".arrow-collapse").forEach((el) => {
            (el as HTMLElement).addEventListener("click", (ev) => {
                if (
                    el
                        .closest("li")
                        ?.querySelector(".collapse")
                        ?.classList.contains("show")
                ) {
                    el.classList.remove("active");
                } else {
                    el.classList.add("active");
                }
                ev.preventDefault();
            });
        });

        window.addEventListener("resize", (ev) => {
            const w = window.innerWidth;
            if (w > 768) {
                if (document.body.classList.contains("offcanvas")) {
                    document.body.classList.remove("offcanvas");
                }
            }
        });

        document.querySelectorAll(".js-burger-toggle-menu").forEach((el) => {
            (el as HTMLElement).addEventListener("click", function (e) {
                e.preventDefault();
                if (document.body.classList.contains("offcanvas")) {
                    document.body.classList.remove("offcanvas");
                    document
                        .querySelectorAll(".js-burger-toggle-menu")
                        .forEach((el) => {
                            el.classList.remove("open");
                        });
                } else {
                    document.body.classList.add("offcanvas");
                    document
                        .querySelectorAll(".js-burger-toggle-menu")
                        .forEach((el) => {
                            el.classList.add("open");
                        });
                }
            });
        });
    }

    function mobileToggleClick() {
        document.querySelectorAll(".js-menu-toggle").forEach((el) => {
            (el as HTMLElement).addEventListener("click", function (e) {
                e.preventDefault();
                const burgers = document.querySelectorAll(
                    ".js-burger-toggle-menu",
                );

                if (document.body.classList.contains("offcanvas")) {
                    document.body.classList.remove("offcanvas");
                    document
                        .querySelectorAll(".js-menu-toggle")
                        .forEach((el) => {
                            el.classList.remove("active");
                        });
                    if (burgers.length) {
                        burgers.forEach((el) => el.classList.remove("open"));
                    }
                } else {
                    document.body.classList.add("offcanvas");

                    document
                        .querySelectorAll(".js-menu-toggle")
                        .forEach((el) => {
                            el.classList.add("active");
                        });
                    if (burgers.length) {
                        burgers.forEach((el) => el.classList.add("open"));
                    }
                }
            });
        });

        // click outisde offcanvas
        document.addEventListener("mouseup", function (e) {
            document
                .querySelectorAll(".unslate_co--site-mobile-menu")
                .forEach((container) => {
                    let isChild = false;
                    for (let child of container.children) {
                        if (child.isEqualNode(e.target as HTMLElement)) {
                            isChild = true;
                            break;
                        }
                    }
                    if (
                        !container.isEqualNode(e.target as Element) &&
                        !isChild
                    ) {
                        if (document.body.classList.contains("offcanvas")) {
                            document.body.classList.remove("offcanvas");
                            document.body
                                .querySelectorAll(".js-menu-toggle")
                                .forEach((el) => {
                                    el.classList.remove("active");
                                });
                            document.body
                                .querySelectorAll(".js-burger-toggle-menu")
                                .forEach((el) => {
                                    el.classList.remove("open");
                                });
                        }
                    }
                });
        });
    }

    function onePageNavigation() {
        // var navToggler = $(".site-menu-toggle");
        document.body
            .querySelectorAll(
                ".unslate_co--site-nav .site-nav-ul li a[href^='#'], .smoothscroll[href^='#'], .unslate_co--site-mobile-menu .site-nav-wrap li a[href^='#']",
            )
            .forEach((el) => {
                (el as HTMLElement).addEventListener("click", function (e) {
                    e.preventDefault();

                    if (document.body.classList.contains("offcanvas")) {
                        document.body.classList.remove("offcanvas");
                        document.body
                            .querySelectorAll(".js-burger-toggle-menu")
                            .forEach((el) => {
                                el.classList.remove("open");
                            });
                    }
                    document.querySelectorAll("html, body").forEach((el) => {
                        el.animate(
                            {
                                scrollTop: el.clientTop,
                            },
                            {
                                duration: 500,
                            },
                        );
                    });
                });
            });
    }

    $effect(() => {
        siteMenuClone();
        mobileToggleClick();
        onePageNavigation();
    });
</script>

<nav class="unslate_co--site-nav site-nav-target">
    <div class="container">
        <div class="row align-items-center justify-content-between text-left">
            <div class="col-md-5 text-right">
                <ul
                    class="site-nav-ul js-clone-nav text-left hidden lg:flex lg:justify-end lg:items-center"
                >
                    <Dropdown options={[
                            {
                                lang: "ES",
                                value: "Español",
                            },
                            {
                                lang: "EN",
                                value: "English",
                            },
                        ]}>
                        {#snippet option_icon(option: { lang: "ES" | "EN" })}
                            {#if option.lang === "ES"}
                                <Es></Es>
                            {:else if option.lang === "EN"}
                                <Gb></Gb>
                            {/if}
                        {/snippet}
                        {#snippet option_label(option)}
                            <span class="w-[50%] text-right">
                                {option.value}
                            </span>
                        {/snippet}
                    </Dropdown>
                    <li>
                        <NavLink href="#home-section" on:click={navigate}>
                            Home
                        </NavLink>
                    </li>
                    <li>
                        <NavLink href="#portfolio-section" on:click={navigate}>
                            Portfolio
                        </NavLink>
                    </li>
                    <li>
                        <NavLink href="#about-section" on:click={navigate}>
                            About
                        </NavLink>
                    </li>
                    <li>
                        <NavLink href="#services-section" on:click={navigate}>
                            Services
                        </NavLink>
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
                    class="site-nav-ul js-clone-nav text-left hidden lg:flex lg:justify-start lg:items-center"
                >
                    <li>
                        <NavLink href="#skills-section" on:click={navigate}>
                            Skills
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            href="#testimonial-section"
                            on:click={navigate}
                        >
                            Testimonial
                        </NavLink>
                    </li>
                    <li>
                        <NavLink href="#journal-section" on:click={navigate}
                            >Journal
                        </NavLink>
                    </li>
                    <li>
                        <NavLink href="#contact-section" on:click={navigate}>
                            Contact
                        </NavLink>
                    </li>
                    <li>
                        <button
                            class={`btn ${$theme === "dark" ? "text-white" : "text-black"}`}
                            onclick={toggleTheme}
                        >
                            {#if $theme === "dark"}
                                <Sun></Sun>
                            {/if}
                            {#if $theme === "light"}
                                <Moon></Moon>
                            {/if}
                        </button>
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
