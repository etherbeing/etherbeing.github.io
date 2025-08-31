<script lang="ts">
    import { createMutation } from "@tanstack/svelte-query";
    import { loginMutation as loginOptions } from "../../../services/auto-openapi/@tanstack/svelte-query.gen";
    import { getContext } from "svelte";
    import { link } from "svelte-spa-router";
    import type { Writable } from "svelte/store";

    const authenticated: Writable<boolean> = getContext("authenticated");

    const loginMutation = createMutation(loginOptions());
    const login = $derived($loginMutation.mutate);
    let username = $state<string>();
    let password = $state<string>();
    $effect(() => {
        if ($loginMutation.isSuccess) {
            authenticated.set(true);
        }
    });
</script>

<div class="container-scroller">
    <div class="container-fluid page-body-wrapper full-page-wrapper">
        <div class="content-wrapper d-flex align-items-center auth px-0">
            <div class="row w-100 mx-0">
                <div class="col-lg-4 mx-auto">
                    <div class="auth-form-light text-left py-5 px-4 px-sm-5">
                        <div class="brand-logo">
                            <img
                                src="/src/assets/dashboard/images/logo.svg"
                                alt="logo"
                            />
                        </div>
                        <h4>Hello! let's get started</h4>
                        <h6 class="font-weight-light">Sign in to continue.</h6>
                        <form
                            class="pt-3"
                            onsubmit={async (event) => {
                                event.preventDefault();
                                event.stopPropagation();
                                if (username && password) {
                                    login({
                                        body: { username, password },
                                        credentials: "include",
                                    });
                                } else {
                                    console.log("Required fields are missing");
                                }
                            }}
                        >
                            <div class="form-group">
                                <input
                                    autocomplete="username"
                                    bind:value={username}
                                    type="text"
                                    class="form-control form-control-lg"
                                    id="username"
                                    placeholder="Username"
                                />
                            </div>
                            <div class="form-group">
                                <input
                                    autocomplete="current-password"
                                    bind:value={password}
                                    type="password"
                                    class="form-control form-control-lg"
                                    id="password"
                                    placeholder="Password"
                                />
                            </div>
                            <div class="mt-3">
                                <button
                                    type="submit"
                                    class="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn"
                                >
                                    SIGN IN
                                </button>
                            </div>
                            <div
                                class="my-2 d-flex justify-content-between align-items-center"
                            >
                                <div class="form-check">
                                    <label class="form-check-label text-muted">
                                        <input
                                            type="checkbox"
                                            class="form-check-input"
                                        />
                                        Keep me signed in
                                    </label>
                                </div>
                                <a href="#" class="auth-link text-black"
                                    >Forgot password?</a
                                >
                            </div>
                            <div class="mb-2">
                                <button
                                    type="button"
                                    class="btn btn-block btn-facebook auth-form-btn"
                                >
                                    <i class="ti-facebook mr-2"></i>Connect
                                    using facebook
                                </button>
                            </div>
                            <div class="text-center mt-4 font-weight-light">
                                Don't have an account? <a
                                    use:link
                                    href="/auth/register/"
                                    class="text-primary">Create</a
                                >
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <!-- content-wrapper ends -->
    </div>
    <!-- page-body-wrapper ends -->
</div>
