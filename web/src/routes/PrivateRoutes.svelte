<script lang="ts">
    import Router from "svelte-spa-router";
    
    

    import NotFound from "../pages/public/unfold-master/NotFound.svelte";
    import AuthGuardian from "../pages/dashboard/skydash-v01/AuthGuardian.svelte";
    import Dashboard from "../pages/dashboard/skydash-v01/Dashboard.svelte";

    const routes = {
        "/dashboard/": Dashboard,
        "*": NotFound,
    };
</script>

<AuthGuardian>
    <Router routes={routes}></Router>
</AuthGuardian>