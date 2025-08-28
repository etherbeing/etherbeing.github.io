<script lang="ts">
    import Router from "svelte-spa-router";
    import DashboardLayout from "./DashboardLayout.svelte";
    import Login from "./Login.svelte";
    import AuthLayout from "./AuthLayout.svelte";

    export const { children } = $props();

    const routes = {
        "*": Login,
    };
    const authenticated = $state(true);
</script>

{#if !authenticated}
    <AuthLayout>
        <Router {routes}></Router>
    </AuthLayout>
{:else}
    <DashboardLayout>
        {@render children?.()}
    </DashboardLayout>
{/if}
