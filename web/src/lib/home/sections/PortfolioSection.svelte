<script lang="ts">
    import { _ } from "svelte-i18n";
    import { link } from "svelte-spa-router";
    import work_1_md from "/src/assets/dark/images/work_1_md.jpg?url";
    import work_2_md from "/src/assets/dark/images/work_2_md.jpg?url";
    import work_3_md from "/src/assets/dark/images/work_3_md.jpg?url";
    import work_4_full from "/src/assets/dark/images/work_4_full.jpg?url";
    import work_5_md from "/src/assets/dark/images/work_5_md.jpg?url";
    import work_6_md from "/src/assets/dark/images/work_6_md.jpg?url";
    import work_7_a_md from "/src/assets/dark/images/work_7_a_md.jpg?url";
    import work_9_a_md from "/src/assets/dark/images/work_9_a_md.jpg?url";
    interface PortfolioItem {
        id: number;
        name: string;
        categories: string[];
        showcase_image_url: string;
        video_url?: string;
        type?: "SimpleImage" | "SimpleVideo" | "Detailed";
    }
    let portfolio_items: Array<PortfolioItem> = $state([
        {
            categories: ["web", "branding"],
            name: "Shoe Rebranding",
            id: 1,
            showcase_image_url: work_1_md,
        },
        {
            categories: ["branding", "packaging", "illustration"],
            name: "Reworking",
            id: 3,
            showcase_image_url: work_2_md,
        },
        {
            categories: ["branding", "packaging"],
            name: "Modern Building",
            id: 4,
            showcase_image_url: work_3_md,
        },
        {
            showcase_image_url: work_4_full,
            type: "SimpleImage",
            id: 100,
            categories: ["web", "packaging"],
            name: "Watch",
        },
        {
            showcase_image_url: work_5_md,
            type: "SimpleImage",
            id: 101,
            categories: ["illustration", "packaging"],
            name: "Shoe Rebranding",
        },
        {
            categories: ["web", "branding"],
            showcase_image_url: work_6_md,
            name: "Reshape",
            id: 2,
        },
        {
            categories: ["branding", "packaging"],
            name: "Modern Building",
            showcase_image_url: work_7_a_md,
            id: 102,
            type: "SimpleImage"
        },
        {
            video_url: "https://www.youtube.com/watch?v=mwtbEGNABWU",
            showcase_image_url: "/src/assets/dark/images/work_8_md.jpg",
            categories: ["web", "branding"],
            name: "Showreel 2019",
            id: 103,
            type: "SimpleVideo"
        },
        {
            showcase_image_url: work_9_a_md,
            categories: ["web", "illustration"],
            name: "Render Packaging",
            id: 104,
            type: "SimpleImage"
        }
    ]);
    let categories = $derived(
        portfolio_items
            .map((portfolio_item, index) => portfolio_item.categories)
            .reduce((p, c) => p.concat(...c.filter((e) => !p.includes(e)))),
    );
</script>

<div class="unslate_co--section" id="portfolio-section">
    <div class="container">
        <div class="relative">
            <div class="loader-portfolio-wrap">
                <div class="loader-portfolio"></div>
            </div>
        </div>
        <div id="portfolio-single-holder"></div>

        <div class="portfolio-wrapper">
            <div
                class="d-flex align-items-center mb-4 gsap-reveal gsap-reveal-filter"
            >
                <h2 class="mr-auto heading-h2">
                    <span class="gsap-reveal">{$_("portfolio.title")}</span>
                </h2>

                <a
                    href="#"
                    class="text-white js-filter d-inline-block d-lg-none"
                    >{$_("portfolio.filter")}</a
                >

                <div class="filter-wrap">
                    <div class="filter ml-auto" id="filters">
                        <a href="#" class="active" data-filter="*">All</a>
                        <a href="#" data-filter=".web">Web</a>
                        <a href="#" data-filter=".branding">Branding</a>
                        <a href="#" data-filter=".illustration">Illustration</a>
                        <a href="#" data-filter=".packaging">Packaging</a>
                    </div>
                </div>
            </div>

            <div id="posts" class="row gutter-isotope-item">
                {#each portfolio_items as portfolio_item}
                    {#if !portfolio_item.type || portfolio_item.type === "Detailed"}
                        <div
                            class="item {portfolio_item.categories.reduce(
                                (p, c) => p.concat(' ', c),
                            )} col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                        >
                            <a
                                href="/portfolio-single-{portfolio_item.id}"
                                use:link
                                class="portfolio-item ajax-load-page isotope-item gsap-reveal-img"
                                data-id={portfolio_item.id}
                            >
                                <div class="overlay">
                                    <span class="wrap-icon icon-link2"></span>
                                    <div class="portfolio-item-content">
                                        <h3>{portfolio_item.name}</h3>
                                        <p>
                                            {#each portfolio_item.categories as category, index}
                                                {category}{#if portfolio_item.categories.length !== index + 1},{/if}
                                            {/each}
                                        </p>
                                    </div>
                                </div>
                                <img
                                    src={portfolio_item.showcase_image_url}
                                    class="lazyload img-fluid"
                                    alt={portfolio_item.name}
                                />
                            </a>
                        </div>
                    {:else if portfolio_item.type === "SimpleImage"}
                        <div
                            class="item {portfolio_item.categories.reduce(
                                (p, c) => p.concat(' ', c),
                            )} col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                        >
                            <a
                                href={portfolio_item.showcase_image_url}
                                class="portfolio-item isotope-item gsap-reveal-img"
                                data-fancybox="gallery"
                                data-caption={portfolio_item.name}
                            >
                                <div class="overlay">
                                    <span class="wrap-icon icon-photo2"></span>
                                    <div class="portfolio-item-content">
                                        <h3>{portfolio_item.name}</h3>
                                        <p>
                                            {#each portfolio_item.categories as category, index}
                                                {category}{#if portfolio_item.categories.length !== index + 1},{/if}
                                            {/each}
                                        </p>
                                    </div>
                                </div>
                                <img
                                    src={portfolio_item.showcase_image_url}
                                    class="lazyload img-fluid"
                                    alt={portfolio_item.name}
                                />
                            </a>
                        </div>
                    {:else if portfolio_item.type === "SimpleVideo"}
                        <div
                            class="item web branding col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                        >
                            <a
                                href={portfolio_item.video_url}
                                class="portfolio-item isotope-item gsap-reveal-img"
                                data-fancybox="gallery"
                                data-caption={portfolio_item.name}
                            >
                                <div class="overlay">
                                    <span
                                        class="wrap-icon icon-play_circle_filled"
                                    ></span>
                                    <div class="portfolio-item-content">
                                        <h3>{portfolio_item.name}</h3>
                                        <p>
                                            {#each portfolio_item.categories as category, index}
                                                {category}{#if portfolio_item.categories.length !== index + 1},{/if}
                                            {/each}
                                        </p>
                                    </div>
                                </div>
                                <img
                                    src={portfolio_item.showcase_image_url}
                                    class="lazyload img-fluid"
                                    alt={portfolio_item.name}
                                />
                            </a>
                        </div>
                    {/if}
                {/each}
            </div>
        </div>
    </div>
</div>
