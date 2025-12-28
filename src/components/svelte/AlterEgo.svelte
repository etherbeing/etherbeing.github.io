<script lang="ts">
    import { init } from "@sentry/astro";
    import { time } from "motion/react";

    const { alter, base }: { alter: string; base: string } = $props();
    let x: number = $state(100);
    let to: number = $state(100);
    const speed = 0.01;
    const acceleration = 1;
    $effect(() => {
        if (x !== to) {
            setTimeout(() => {
                const initial = x;
                if (x < to) {
                    x += acceleration;
                } else if (x > to) {
                    x -= acceleration;
                } else {
                    return;
                }
                if (initial < to && x > to) {
                    x = to;
                } else if (initial > to && x < to) {
                    x = to;
                }
            }, speed);
        }
    });
    let ref = $state();
</script>

<div
    role="img"
    bind:this={ref}
    class={"max-h-[60%] h-full w-full overflow-hidden relative -z-10 left-0 top-0"}
    onfocus={null}
    onmouseenter={(e) => {
        to = (e.offsetX * 100) / e.currentTarget.clientWidth;
    }}
    onmousemove={(e) => {
        to = (e.offsetX * 100) / e.currentTarget.clientWidth;
    }}
    onmouseleave={(e) => {
        to = (e.offsetX * 100) / e.currentTarget.clientWidth > 50?100:0;
    }}
>
    <img
        alt={"base"}
        src={base}
        class="absolute left-0 top-0 min-h-full w-full"
    />
    <img
        alt={"alter"}
        src={alter}
        class="absolute left-0 top-0 min-h-full w-full"
        style="mask-image: linear-gradient(to right, transparent 0%, transparent {x}%, black {x}%, black 100%)"
    />
</div>
