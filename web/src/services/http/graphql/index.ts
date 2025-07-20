import { Client, cacheExchange, fetchExchange, setContextClient } from '@urql/svelte';

export const client = new Client({
    url: new URL('graphql', import.meta.env.VITE_BACKEND_URL).toString(),
    exchanges: [cacheExchange, fetchExchange],
    fetchOptions: () => {
        // const token = getToken();
        return {
            headers: {
                // authorization: token ? `Bearer ${token}` : '' 
            },
        };
    },
});
