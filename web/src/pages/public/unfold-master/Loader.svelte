<script lang="ts">
    import gsap from "gsap";
    import { Power4 } from "gsap";

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
    $effect(() => {
        dismissLoader();
    });
</script>

<div id="unslate_co--overlayer"></div>
<div class="site-loader-wrap">
    <div class="site-loader"></div>
</div>
