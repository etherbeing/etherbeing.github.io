<script lang="ts">
    import {
        createQuery,
        type CreateQueryResult,
    } from "@tanstack/svelte-query";
    import { getInfoAboutMeOptions } from "../../../services/auto-openapi/@tanstack/svelte-query.gen";
    import type { AboutMe } from "../../../services/auto-openapi";
    const publicInfo = createQuery(
        getInfoAboutMeOptions(),
    ) as CreateQueryResult<AboutMe>;
</script>

{#if $publicInfo.isLoading}
    <div class="flex justify-center min-h-screen items-center">Loading...</div>
{:else if $publicInfo.isSuccess}
    <div class="cover-v1 overlay jarallax-video" id="home-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-7 mx-auto text-center">
                    <h1 class="heading gsap-reveal-hero text-white">
                        {$publicInfo.data.name}
                    </h1>
                    <h2 class="subheading gsap-reveal-hero text-white">
                        {$publicInfo.data.pitch}
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
{:else if $publicInfo.isError}
    <div class="cover-v1 overlay jarallax-video" id="home-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-7 mx-auto text-center">
                    <h1 class="heading gsap-reveal-hero text-white">
                        etherbeing
                    </h1>
                    <h2 class="subheading gsap-reveal-hero text-white">
                        Let's build the impossible
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
    <!-- <div class="flex justify-center min-h-screen items-center">
        An error occurred communicating with the backend (is probably not available as I am deciding yet which provider to use to deploy it)
    </div> -->
{/if}
