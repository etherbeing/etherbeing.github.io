<script lang="ts">
    import { push, params, location } from "svelte-spa-router";
    import type { Snippet } from "svelte";
    import { getContext } from "svelte";
    import { createMutation, createQuery } from "@tanstack/svelte-query";
    import {
        meOptions,
        refreshMutation,
    } from "../../../services/auto-openapi/@tanstack/svelte-query.gen";
    import { type Writable } from "svelte/store";

    const { children }: { children: Snippet } = $props();
    const currentUserQuery = createQuery(meOptions({ credentials: "include" }));
    const refresh = createMutation(refreshMutation({ credentials: "include" }));
    let authenticated: Writable<boolean> = getContext("authenticated");

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
    const DEFAULT_AUTH_ROUTE = "/auth/login/";

    $effect(() => {
        if (!$authenticated && $location != DEFAULT_AUTH_ROUTE) {
            push(`${DEFAULT_AUTH_ROUTE}?to=${$location}`);
        } else if ($authenticated && $location.startsWith("/auth/")) {
            push($params?.to || "/admin/dashboard/");
        }
    });
</script>

{#if $authenticated}
    {@render children?.()}
{/if}
