<script lang="ts">
    import { createQuery } from "@tanstack/svelte-query";
    import { getContext, onMount } from "svelte";
    import type { Writable } from "svelte/store";
    import { getInfoAboutMeOptions } from "../../../services/auto-openapi/@tanstack/svelte-query.gen";
    const theme: Writable<"light" | "dark"> = getContext("theme");
    const publicInfo = createQuery(getInfoAboutMeOptions());
</script>

{#if $publicInfo.isLoading }
    Loading...
{:else if $publicInfo.isSuccess}
    <div class="cover-v1 overlay jarallax-video" id="home-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-7 mx-auto text-center">
                    <h1 class="heading gsap-reveal-hero text-white">{$publicInfo.data.name}</h1>
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
    <div>
        An error occurred
    </div>
{/if}
