<script lang="ts">
    import { _ } from "svelte-i18n";
    import divider from "/src/assets/dark/images/divider.png?url";
    import { contactMutation } from "../../../services/auto-openapi/@tanstack/svelte-query.gen";
    import type { FormEventHandler } from "svelte/elements";
    import { onMount } from "svelte";
    import { gsap } from "gsap";
    import { createMutation } from "@tanstack/svelte-query";

    const cm = createMutation(contactMutation());

    let form: HTMLFormElement;
    let successMsg: HTMLDivElement;
    let disabled: boolean = $state(false);
    let name: string = $state("");
    let email: string = $state("");
    let message: string = $state("");

    function labelAnim(el: HTMLElement, force: boolean = false) {
        const label = el.parentElement?.querySelector("label");
        if (!label) {
            return;
        }
        if ((el as HTMLInputElement).value || force) {
            // @ts-expect-error
            el.parentElement.classList.add("overflow-visible!");

            gsap.to(label, {
                y: -20,
                duration: 0.1,
                ease: "bounce.out",
                // position: 'relative'
            });
        } else {
            gsap.to(label, {
                y: 0,
                duration: 0.1,
                ease: "bounce.in",
                // position: 'relative'
            }).then(() => {
                el.parentElement?.classList.remove("overflow-visible!");
            });
        }
    }

    onMount(() => {
        document
            .querySelectorAll("#contact-section .form-control")
            .forEach((el) => {
                (el as HTMLLabelElement).addEventListener("change", () =>
                    labelAnim(el as HTMLElement),
                );
                (el as HTMLLabelElement).addEventListener("focus", () =>
                    labelAnim(el as HTMLElement, true),
                );
                (el as HTMLLabelElement).addEventListener("blur", () =>
                    labelAnim(el as HTMLElement),
                );
            });
    });

    var onContact: FormEventHandler<HTMLFormElement> = async function (event) {
        event.preventDefault();
        if (!event.target) return;
        disabled = true;
        await $cm.mutate(
            {
                body: {
                    name,
                    email,
                    message,
                },
            },
            {
                onSuccess: (data, variables, context) => {
                    // if (msg == "OK") {
                    //     $("#form-message-warning").hide();
                    //     setTimeout(function () {
                    //         $("#contactForm").fadeOut();
                    //     }, 1000);
                    //     setTimeout(function () {
                    //         $("#form-message-success").fadeIn();
                    //     }, 1400);
                    // } else {
                    //     $("#form-message-warning").html(msg);
                    //     $("#form-message-warning").fadeIn();
                    //     $submit.css("display", "none");
                    // }
                    console.log("coool");
                    gsap.to(form, {
                        x: "-100vw",
                    }).then(()=>{
                        form.classList.toggle("hidden", true);
                        gsap.fromTo(successMsg, {x: "-100vw", display: "flex"}, {x: "0"})
                    });
                    name = "";
                    email = "";
                    message = "";
                },
                onError: (error) => {
                    console.log("not so coool");
                    // $("#form-message-warning").html(
                    //     "Something went wrong. Please try again.",
                    // );
                    // $("#form-message-warning").fadeIn();
                    // $submit.css("display", "none");
                },
            },
        );
        disabled = false;
    };
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
                    bind:this={form}
                    method="post"
                    class="form-outline-style-v1"
                    onsubmit={onContact}
                >
                    <div class="form-group row mb-0">
                        <div class="col-lg-6 form-group gsap-reveal">
                            <label for="name">{$_("contact.name")}</label>
                            <input
                                name="name"
                                bind:value={name}
                                type="text"
                                class="form-control"
                                id="name"
                                required
                            />
                        </div>
                        <div class="col-lg-6 form-group gsap-reveal">
                            <label for="email">{$_("contact.email")}</label>
                            <input
                                bind:value={email}
                                name="email"
                                type="email"
                                class="form-control"
                                id="email"
                                required
                            />
                        </div>
                        <div class="col-lg-12 form-group gsap-reveal">
                            <label for="message">{$_("contact.write")}</label>
                            <textarea
                                bind:value={message}
                                name="message"
                                id="message"
                                required
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
                                {disabled}
                                class="btn btn-outline-pill btn-custom-light mr-3"
                                value={disabled
                                    ? $_("contact.submitting")
                                    : $_("contact.send")}
                            />
                            <span class="submitting"></span>
                        </div>
                    </div>
                </form>
                <div id="form-message-warning" class="mt-4"></div>
                <div id="form-message-success" class="justify-center items-center h-full w-full" bind:this={successMsg}>
                    {$_("contact.success")}
                </div>
            </div>

            <div class="col-md-4">
                <div class="contact-info-v1">
                    <div class="gsap-reveal d-block">
                        <span class="d-block contact-info-label"
                            >{$_("contact.email")}</span
                        >
                        <a
                            href="mailto:etherbeing99@proton.me"
                            class="contact-info-val">etherbeing99@proton.me</a
                        >
                    </div>
                    <div class="gsap-reveal d-block">
                        <span class="d-block contact-info-label"
                            >{$_("contact.phone")}</span
                        >
                        <a href="tel://+46764039298" class="contact-info-val"
                            >+46 76 403 9298</a
                        >
                    </div>
                    <div class="gsap-reveal d-block">
                        <span class="d-block contact-info-label"
                            >{$_("contact.address")}</span
                        >
                        <address class="contact-info-val">
                            Stockholm, Sweden
                        </address>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
