
import { QueryClient } from "@tanstack/svelte-query";

export const baseQuery = new QueryClient();

async function baseFetch(path: string) {
    const result = await fetch(
        new URL(path, import.meta.env.VITE_BACKEND_URL),
        {
            headers: {
                Authorization: "Bearer header",
            },
        },
    );
    try {
        return result.json();
    } catch {
        return result.body;
    }
}

export const demoQuery = async () => {
    const result = await baseFetch("/");
    return result as {
        message: string;
    };
};
