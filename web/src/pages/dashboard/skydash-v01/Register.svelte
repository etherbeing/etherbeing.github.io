<script lang="ts">
  import { createMutation } from "@tanstack/svelte-query";
  import { link } from "svelte-spa-router";
  import { registerMutation } from "../../../services/auto-openapi/@tanstack/svelte-query.gen";
  import { getContext } from "svelte";
  import { type Writable } from "svelte/store";

  let username: string|undefined = $state();
  let email: string|undefined = $state();
  let country: number|undefined = $state();
  let password: string|undefined = $state();
  const register = createMutation(registerMutation());
  let authenticated: Writable<boolean> = getContext("authenticated");
</script>

<div class="container-scroller">
  <div class="container-fluid page-body-wrapper full-page-wrapper">
    <div class="content-wrapper d-flex align-items-center auth px-0">
      <div class="row w-100 mx-0">
        <div class="col-lg-4 mx-auto">
          <div class="auth-form-light text-left py-5 px-4 px-sm-5">
            <div class="brand-logo">
              <img src="/src/assets/dashboard/images/logo.svg" alt="logo" />
            </div>
            <h4>New here?</h4>
            <h6 class="font-weight-light">
              Signing up is easy. It only takes a few steps
            </h6>
            <form
              class="pt-3"
              onsubmit={(ev) => {
                ev.preventDefault();
                ev.stopPropagation();
                $register.mutate(
                  {
                    body: {
                      username: username as string,
                      password: password as string,
                      email: email as string,
                      country: country as number,
                    },
                  },
                  {
                    onSuccess: () => authenticated.set(true),
                  },
                );
              }}
            >
              <div class="form-group">
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="username"
                  name="username"
                  placeholder="Username"
                  bind:value={username}
                />
              </div>
              <div class="form-group">
                <input
                  type="email"
                  class="form-control form-control-lg"
                  id="email"
                  placeholder="Email"
                  name="email"
                  bind:value={email}
                />
              </div>
              <div class="form-group">
                <select
                  class="form-control form-control-lg"
                  id="country"
                  name="country"
                  bind:value={country}
                >
                  <option value={undefined}>Country</option>
                  <option value={0}>United States of America</option>
                  <option value={1}>United Kingdom</option>
                  <option value={2}>India</option>
                  <option value={3}>Germany</option>
                  <option value={4}>Argentina</option>
                </select>
              </div>
              <div class="form-group">
                <input
                  type="password"
                  class="form-control form-control-lg"
                  id="password"
                  name="password"
                  bind:value={password}
                  placeholder="Password"
                />
              </div>
              <div class="mb-4">
                <div class="form-check">
                  <label class="form-check-label text-muted">
                    <input type="checkbox" class="form-check-input" />
                    I agree to all Terms & Conditions
                  </label>
                </div>
              </div>
              <div class="mt-3">
                <button
                  class="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn"
                >
                  SIGN UP
                </button>
              </div>
              <div class="text-center mt-4 font-weight-light">
                Already have an account? <a
                  use:link
                  href="/auth/login/"
                  class="text-primary">Login</a
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
