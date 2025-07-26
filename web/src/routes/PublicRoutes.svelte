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
    import Layout from "../pages/public/unfold-master/Layout.svelte";
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
        "/": Home, // remember hash routing starts with /#/
        "/blog-single/:id": BlogSingle,
        "/portfolio-single-1": PortfolioSingle1,
        "/portfolio-single-2": PortfolioSingle2,
        "/portfolio-single-3": PortfolioSingle3,
        "/portfolio-single-4": PortfolioSingle4,
        "/copyright": Copyright,
        "*": NotFound,
    };
</script>

<Layout>
    <Router {routes}></Router>
</Layout>
