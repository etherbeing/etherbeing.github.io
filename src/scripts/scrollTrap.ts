import { gsap } from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function initScrollManager(sections_ids: string[]) {
    sections_ids.map(id => document.getElementById(id)).forEach((section, i, array) => {

        const next = array[i + 1]; // optional for end boundary

        gsap.fromTo(
            section,
            { scale: 0.6 },    // when not visible / before entering
            {
                scale: 1,    // while centered in viewport
                ease: "none",
                scrollTrigger: {
                    trigger: section,
                    endTrigger: next || section, // last one falls back to itself
                    scrub: true,
                    start: "top 50%",   // begins scaling when top touches bottom of screen
                    end: "bottom top",     // back to shrink when leaving
                    // markers: true,      // enable for debugging
                    onUpdate: self => {
                        // shrink back near exit
                        const progress = self.progress;
                        const scale = progress < 0.5
                            ? gsap.utils.interpolate(0.6, 1.2, progress * 2)      // enter zoom
                            : gsap.utils.interpolate(1.2, 0.6, (progress - 0.5) * 2); // exit shrink
                        gsap.set(section, { scale });
                    }
                }
            }
        );
    });
}
