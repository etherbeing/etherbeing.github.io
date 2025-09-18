<script lang="ts">
    import { link } from "svelte-spa-router";
    import divider from "/src/assets/dark/images/divider.png";
    import post_1 from "/src/assets/dark/images/post_1.jpg?url";
    import post_2 from "/src/assets/dark/images/post_2.jpg?url";
    import post_3 from "/src/assets/dark/images/post_3.jpg?url";
    import post_4 from "/src/assets/dark/images/post_4.jpg?url";
    import post_5 from "/src/assets/dark/images/post_5.jpg?url";

    interface BlogPost {
        title: string;
        author: string;
        herd: string; // humanized estimated read duration
        cover_image: string;
    }

    let posts: Array<BlogPost> = $state([
        {
            title: "A Mounteering Guide For Beginners",
            author: "Joefrey",
            herd: "5 mins",
            cover_image: post_1,
        },
        {
            title: "A Mounteering Guide For Beginners",
            author: "Joefrey",
            herd: "5 mins",
            cover_image: post_2,
        },
        {
            title: "A Mounteering Guide For Beginners",
            author: "Joefrey",
            herd: "5 mins",
            cover_image: post_3,
        },
        {
            title: "A Mounteering Guide For Beginners",
            author: "Joefrey",
            herd: "5 mins",
            cover_image: post_4,
        },
        {
            title: "A Mounteering Guide For Beginners",
            author: "Joefrey",
            herd: "5 mins",
            cover_image: post_5,
        },
    ]);
</script>

<div class="unslate_co--section" id="journal-section">
    <div class="container">
        <div class="section-heading-wrap text-center mb-5">
            <h2 class="heading-h2 text-center divider">
                <span class="gsap-reveal">My Journal</span>
            </h2>
            <span class="gsap-reveal"
                ><img src={divider} alt="divider" width="76" /></span
            >
        </div>

        <div class="row gutter-v4 align-items-stretch">
            {#each posts as post, index}
                <div
                    class="col-sm-6 col-md-6 col-lg-{index === 0
                        ? 8
                        : 4} blog-post-entry"
                    data-aos="fade-up"
                    data-aos-delay={index * 100}
                >
                    <a
                        href="/blog-single"
                        use:link
                        class="grid-item blog-item w-100 h-100"
                    >
                        <div class="overlay">
                            <div class="portfolio-item-content">
                                <h3>{post.title}</h3>
                                <p class="post-meta">
                                    By {post.author}
                                    <span class="small">&bullet;</span>
                                    {post.herd} read
                                </p>
                            </div>
                        </div>
                        <img
                            src={post.cover_image}
                            class="lazyload"
                            alt={post.title}
                        />
                    </a>
                </div>
            {/each}
        </div>
    </div>
</div>
<!-- END blog posts -->
