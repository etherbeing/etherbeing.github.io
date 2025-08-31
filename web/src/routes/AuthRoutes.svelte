<script lang="ts">
    import Router, { params, push, location } from "svelte-spa-router";
    import AuthLayout from "../pages/dashboard/skydash-v01/AuthLayout.svelte";

    import Login from "../pages/dashboard/skydash-v01/Login.svelte";
    import Register from "../pages/dashboard/skydash-v01/Register.svelte";
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import { createQuery, createMutation } from "@tanstack/svelte-query";
    import {
        meOptions,
        refreshMutation,
    } from "../services/auto-openapi/@tanstack/svelte-query.gen";

    const routes = {
        "*/login/": Login,
        "*/register/": Register,
        // "*": Login,
    };

    const currentUserQuery = createQuery(meOptions({ credentials: "include" }));
    const refresh = createMutation(refreshMutation({ credentials: "include" }));
    const authenticated: Writable<boolean> = getContext("authenticated");

    $effect(() => {
        if ($currentUserQuery.isFetched) {
            if ($currentUserQuery.isSuccess) {
                authenticated.set(true);
            } else if (
                $currentUserQuery.isError &&
                !$currentUserQuery.isFetching
            ) {
                if (!$refresh.isPending && !$refresh.isError) {
                    $refresh.mutate(
                        {},
                        {
                            onSuccess: () => {
                                authenticated.set(true);
                                $currentUserQuery.refetch();
                            },
                            onError: () => authenticated.set(false),
                        },
                    );
                }
            }
        }
    });

    $effect(() => {
        if ($authenticated) {
            push($params?.to || "/admin/dashboard/");
        }
    });
</script>

{#if !$authenticated}
    <AuthLayout>
        <Router {routes}></Router>
    </AuthLayout>
{/if}
