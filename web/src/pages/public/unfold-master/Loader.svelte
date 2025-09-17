<script lang="ts">
    import gsap from "gsap";
    import { Power4 } from "gsap";
    import { isLoading, waitLocale } from "svelte-i18n";
    import { REFRESH_UNFOLD_CONTEXT_NAME } from "../../../consts";
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";

    function dismissLoader() {
        gsap.to(".site-loader-wrap", {
            autoAlpha: 0,
            marginTop: 50,
            y: 100,
            ease: Power4.easeInOut,
        })
            .delay(1)
            .duration(1)
            .then((el) => {
                gsap.to(".site-loader-wrap", { opacity: 0 })
                    .duration(1.5)
                    .delay(0.2);
                gsap.to("#unslate_co--overlayer", {
                    opacity: 0,
                })
                    .duration(1.5)
                    .delay(0.2);
            });
    }
    interface Stage {
        label: string;
        loading: boolean;
    }
    let stages: Stage[] = $state([
        {
            label: "Loading locales",
            loading: $isLoading,
        },
    ]);
    const refreshUnfold: Writable<Function> = getContext(
        REFRESH_UNFOLD_CONTEXT_NAME,
    );
    let current_stage: Stage | undefined = $state();
    $effect(() => {
        if (!current_stage?.loading && stages.length) {
            current_stage = stages.pop();
        }
    });
    $effect(() => {
        if (!stages.length) {
            dismissLoader();
            $refreshUnfold();
        }
    });
</script>

<div id="unslate_co--overlayer"></div>
<div class="site-loader-wrap">
    <div class="site-loader"></div>
    {#if current_stage?.loading}
        {current_stage.label}
    {/if}
</div>
