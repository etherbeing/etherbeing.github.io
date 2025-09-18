<script lang="ts">
    import divider from "/src/assets/dark/images/divider.png";
    import person_man_1 from "/src/assets/dark/images/person_man_1.jpg?url";
    import person_woman_1 from "/src/assets/dark/images/person_woman_1.jpg?url";
    import person_man_2 from "/src/assets/dark/images/person_man_2.jpg?url";

    interface Testimonial {
        content: string;
        name: string;
        role: string;
        avatar: string;
    }
    let testimonials: Array<Testimonial> = $state([
        {
            content: `Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.`,
            avatar: person_man_1,
            name: "Eric Ingram",
            role: "Product Designer @facebook",
        },
        {
            content: `Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.`,
            avatar: person_man_2,
            name: "Ryan Mullins",
            role: "Product Designer @Shopify",
        },
        {
            content: `Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.`,
            avatar: person_woman_1,
            name: "Erica Miller",
            role: "Product Designer @Twitter",
        },
    ]);
</script>

<div class="unslate_co--section" id="testimonial-section">
    <div class="container">
        <div class="section-heading-wrap text-center mb-5">
            <h2 class="heading-h2 text-center divider">
                <span class="gsap-reveal">My Happy Clients</span>
            </h2>
            <span class="gsap-reveal">
                <img src={divider} alt="divider" width="76" />
            </span>
        </div>
    </div>

    <div class="owl-carousel testimonial-slider" data-aos="fade-up">
        {#each testimonials as testimonial}
            <div>
                <div class="testimonial-v1">
                    <div class="testimonial-inner-bg">
                        <span class="quote">&ldquo;</span>
                        <blockquote>{testimonial.content}</blockquote>
                    </div>

                    <div class="testimonial-author-info">
                        <img src={testimonial.avatar} alt={testimonial.name} />
                        <h3>{testimonial.name}</h3>
                        <span class="d-block position">{testimonial.role}</span>
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>
<!-- END testimonial -->
