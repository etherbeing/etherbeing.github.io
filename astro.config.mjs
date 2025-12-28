// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import icon from "astro-icon";

import react from "@astrojs/react";

import svelte from "@astrojs/svelte";

import sentry from "@sentry/astro";
import spotlightjs from "@spotlightjs/astro";

// https://astro.build/config
export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
    server: {
      watch: {
        ignored: [
          "api/**",
          "node_modules/**",
          "target/**",
          "high_performance/**",
          "devops/**",
          "dist/**"
        ]
      }
    }
  },
  output: "static",
  integrations: [
    icon(),
    react(),
    svelte(),
    sentry(),
    spotlightjs()
  ],
});
