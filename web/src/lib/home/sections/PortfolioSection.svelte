<script lang="ts">
    import { link } from "svelte-spa-router";
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
                    <span class="gsap-reveal">Portfolio</span>
                </h2>

                <!-- <a href="#" class="text-white js-filter d-inline-block d-lg-none">Filter</a>
                  
                  <div class="filter-wrap">
                    <div class="filter ml-auto" id="filters">
                      <a href="#" class="active" data-filter="*">All</a>
                      <a href="#" data-filter=".web">Web</a>
                      <a href="#" data-filter=".branding">Branding</a>
                      <a href="#" data-filter=".illustration">Illustration</a>
                      <a href="#" data-filter=".packaging">Packaging</a>
                    </div>
                  </div> -->
            </div>

            <div id="posts" class="row gutter-isotope-item">
                <div
                    class="item web branding col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="/portfolio-single-1"
                        use:link
                        class="portfolio-item ajax-load-page isotope-item gsap-reveal-img"
                        data-id="1"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-link2"></span>
                            <div class="portfolio-item-content">
                                <h3>Shoe Rebranding</h3>
                                <p>web, branding</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_1_md.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>
                <div
                    class="item branding packaging illustration col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="/portfolio-single-3"
                        use:link
                        class="portfolio-item ajax-load-page item-portrait isotope-item gsap-reveal-img"
                        data-id="3"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-link2"></span>
                            <div class="portfolio-item-content">
                                <h3>Reworking</h3>
                                <p>branding, packaging, illustration</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_2_md.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>

                <div
                    class="item branding packaging col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="/portfolio-single-4"
                        use:link
                        class="portfolio-item isotope-item gsap-reveal-img ajax-load-page"
                        data-id="4"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-link2"></span>
                            <div class="portfolio-item-content">
                                <h3>Modern Building</h3>
                                <p>branding, packaging</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_3_md.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>

                <div
                    class="item web packaging col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="/src/assets/dark/images/work_4_full.jpg"
                        class="portfolio-item isotope-item gsap-reveal-img"
                        data-fancybox="gallery"
                        data-caption="Watch"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-photo2"></span>
                            <div class="portfolio-item-content">
                                <h3>Watch</h3>
                                <p>web, packaging</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_4_full.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>

                <div
                    class="item illustration packaging col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="/src/assets/dark/images/work_5_md.jpg"
                        class="portfolio-item isotope-item gsap-reveal-img"
                        data-fancybox="gallery"
                        data-caption="Shoe Rebranding"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-photo2"></span>
                            <div class="portfolio-item-content">
                                <h3>Shoe Rebranding</h3>
                                <p>illustration, packaging</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_5_md.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>

                <div
                    class="item web branding col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="/portfolio-single-2"
                        use:link
                        class="portfolio-item ajax-load-page item-portrait isotope-item gsap-reveal-img"
                        data-id="2"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-link2"></span>
                            <div class="portfolio-item-content">
                                <h3>Reshape</h3>
                                <p>web, branding</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_6_md.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>

                <div
                    class="item branding packaging col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="/src/assets/dark/images/work_7_a_md.jpg"
                        class="portfolio-item item-portrait isotope-item gsap-reveal-img"
                        data-fancybox="gallery"
                        data-caption="Modern Building"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-photo2"></span>
                            <div class="portfolio-item-content">
                                <h3>Modern Building</h3>
                                <p>branding, packaging</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_7_a_md.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>

                <div
                    class="item web branding col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="https://www.youtube.com/watch?v=mwtbEGNABWU"
                        class="portfolio-item isotope-item gsap-reveal-img"
                        data-fancybox="gallery"
                        data-caption="Showreel 2019"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-play_circle_filled"
                            ></span>
                            <div class="portfolio-item-content">
                                <h3>Showreel 2019</h3>
                                <p>web, branding</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_8_md.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>

                <div
                    class="item web illustration col-sm-6 col-md-6 col-lg-4 isotope-mb-2"
                >
                    <a
                        href="/src/assets/dark/images/work_9_a_md.jpg"
                        class="portfolio-item isotope-item gsap-reveal-img"
                        data-fancybox="gallery"
                        data-caption="Render Packaging"
                    >
                        <div class="overlay">
                            <span class="wrap-icon icon-photo2"></span>
                            <div class="portfolio-item-content">
                                <h3>Render Packaging</h3>
                                <p>web, illustration</p>
                            </div>
                        </div>
                        <img
                            src="/src/assets/dark/images/work_9_a_md.jpg"
                            class="lazyload img-fluid"
                            alt="Images"
                        />
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
