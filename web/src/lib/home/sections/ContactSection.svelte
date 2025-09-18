<script lang="ts">
    import { _ } from "svelte-i18n";
    import divider from "/src/assets/dark/images/divider.png?url";

</script>
<div class="unslate_co--section" id="contact-section">
    <div class="container">
        <div class="section-heading-wrap text-center mb-5">
            <h2 class="heading-h2 text-center divider">
                <span class="gsap-reveal">{$_("contact.title")}</span>
            </h2>
            <span class="gsap-reveal"
                ><img src={divider} alt="divider" width="76" /></span
            >
        </div>

        <div class="row justify-content-between">
            <div class="col-md-6">
                <form
                    method="post"
                    class="form-outline-style-v1"
                    id="contactForm"
                >
                    <div class="form-group row mb-0">
                        <div class="col-lg-6 form-group gsap-reveal">
                            <label for="name">{$_("contact.name")}</label>
                            <input
                                name="name"
                                type="text"
                                class="form-control"
                                id="name"
                            />
                        </div>
                        <div class="col-lg-6 form-group gsap-reveal">
                            <label for="email">{$_("contact.email")}</label>
                            <input
                                name="email"
                                type="email"
                                class="form-control"
                                id="email"
                            />
                        </div>
                        <div class="col-lg-12 form-group gsap-reveal">
                            <label for="message">{$_("contact.write")}</label>
                            <textarea
                                name="message"
                                id="message"
                                cols="30"
                                rows="7"
                                class="form-control"
                            ></textarea>
                        </div>
                    </div>
                    <div class="form-group row gsap-reveal">
                        <div class="col-md-12 d-flex align-items-center">
                            <input
                                type="submit"
                                class="btn btn-outline-pill btn-custom-light mr-3"
                                value={$_("contact.send")}
                            />
                            <span class="submitting"></span>
                        </div>
                    </div>
                </form>
                <div id="form-message-warning" class="mt-4"></div>
                <div id="form-message-success">
                    {$_("contact.success")}
                </div>
            </div>

            <div class="col-md-4">
                <div class="contact-info-v1">
                    <div class="gsap-reveal d-block">
                        <span class="d-block contact-info-label">{$_("contact.email")}</span>
                        <a href="mailto:etherbeing99@proton.me" class="contact-info-val"
                            >etherbeing99@proton.me</a
                        >
                    </div>
                    <div class="gsap-reveal d-block">
                        <span class="d-block contact-info-label">{$_("contact.phone")}</span>
                        <a href="tel://+46764039298" class="contact-info-val">+46 76 403 9298</a
                        >
                    </div>
                    <div class="gsap-reveal d-block">
                        <span class="d-block contact-info-label">{$_("contact.address")}</span>
                        <address class="contact-info-val">
                            Stockholm, Sweden
                        </address>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
