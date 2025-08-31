<script lang="ts">
    import Router, { location } from "svelte-spa-router";
    import PrivateRoutes from "./PrivateRoutes.svelte";
    import PublicRoutes from "./PublicRoutes.svelte";
    import { getContext } from "svelte";
    import { REFRESH_UNFOLD_CONTEXT_NAME } from "../consts";
    import type { Writable } from "svelte/store";
    import AuthRoutes from "./AuthRoutes.svelte";

    const refreshUnfold: Writable<() => void> = getContext(
        REFRESH_UNFOLD_CONTEXT_NAME,
    );
    location.subscribe(() => {
        setTimeout(() => { // TODO watch me in case of errors
            // this is needed in order to assume the page is loaded just in time before attempting to access the DOM...
            $refreshUnfold();
        }, 0);
    });

    const routes = {
        "/admin/*": PrivateRoutes,
        "/auth/*": AuthRoutes,
        "/*": PublicRoutes,
    };
</script>

<Router {routes} prefix=""></Router>
