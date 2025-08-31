import {defineConfig} from "@hey-api/openapi-ts";

export default defineConfig({
    input: "http://localhost:8080/api-doc/openapi.json",
    output: "src/services/auto-openapi/",
    plugins: [
        "@tanstack/svelte-query",
    ],
})