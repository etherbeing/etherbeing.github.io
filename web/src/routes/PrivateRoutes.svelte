<script lang="ts">
    import Router from "svelte-spa-router";

    import AuthGuardian from "../pages/dashboard/skydash-v01/AuthGuardian.svelte";
    import Dashboard from "../pages/dashboard/skydash-v01/Dashboard.svelte";
    import Error404 from "../pages/dashboard/skydash-v01/Error404.svelte";
    import Buttons from "../pages/dashboard/skydash-v01/Buttons.svelte";
    import Dropdowns from "../pages/dashboard/skydash-v01/Dropdowns.svelte";
    import Typography from "../pages/dashboard/skydash-v01/Typography.svelte";
    import BasicTable from "../pages/dashboard/skydash-v01/BasicTable.svelte";
    import Mdi from "../pages/dashboard/skydash-v01/MDI.svelte";
    import BasicElements from "../pages/dashboard/skydash-v01/BasicElements.svelte";
    import Chartjs from "../pages/dashboard/skydash-v01/Chartjs.svelte";

    const routes = {
        "*/dashboard/": Dashboard,
        "*/buttons/": Buttons,
        "*/dropdowns/": Dropdowns,
        "*/typography/": Typography,
        "*/basic-table/": BasicTable,
        "*/mdi/": Mdi,
        "*/basic-elements/": BasicElements,
        "*/chartjs/": Chartjs,
        "*": Error404,
    };
</script>

<AuthGuardian>
    <Router {routes}></Router>
</AuthGuardian>
