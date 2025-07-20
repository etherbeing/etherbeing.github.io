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
</script>

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
<!-- END .cover-v1 -->
