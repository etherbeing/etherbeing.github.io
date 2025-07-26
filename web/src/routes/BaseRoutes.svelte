<script lang="ts">
    import Router, { location } from "svelte-spa-router";
    import Home from "../pages/public/unfold-master/Home.svelte";
    import BlogSingle from "../pages/public/unfold-master/BlogSingle.svelte";
    import PortfolioSingle1 from "../pages/public/unfold-master/PortfolioSingle1.svelte";
    import PortfolioSingle2 from "../pages/public/unfold-master/PortfolioSingle2.svelte";
    import PortfolioSingle3 from "../pages/public/unfold-master/PortfolioSingle3.svelte";
    import PortfolioSingle4 from "../pages/public/unfold-master/PortfolioSingle4.svelte";
    import Copyright from "../pages/public/unfold-master/Copyright.svelte";
    import NotFound from "../pages/public/unfold-master/NotFound.svelte";
    import PrivateRoutes from "./PrivateRoutes.svelte";
    import PublicRoutes from "./PublicRoutes.svelte";
    import { getContext } from "svelte";
    import { REFRESH_UNFOLD_CONTEXT_NAME } from "../consts";
    import type { Writable } from "svelte/store";

    const refreshUnfold: Writable<() => void> = getContext(
        REFRESH_UNFOLD_CONTEXT_NAME,
    );
    location.subscribe((val) => {
        setTimeout(() => { // TODO watch me in case of errors
            // this is needed in order to assume the page is loaded just in time before attempting to access the DOM...
            $refreshUnfold();
        }, 0);
    });

    const routes = {
        "/admin/*": PrivateRoutes,
        "/*": PublicRoutes,
    };
</script>

<Router {routes}></Router>
