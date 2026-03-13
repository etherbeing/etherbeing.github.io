import type { APIRoute } from "astro";
import { fetchSiteConfiguration } from "@/lib/siteConfiguration";

export const prerender = true;

export const GET: APIRoute = async () => {
  const configuration = await fetchSiteConfiguration(import.meta.env.PUBLIC_API_URL);
  const manifest = {
    name: configuration.site_name,
    short_name: configuration.short_name,
    description: configuration.site_description,
    start_url: "/",
    display: "standalone",
    background_color: configuration.background_color,
    theme_color: configuration.theme_color,
    icons: [
      {
        src: configuration.favicon_url,
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: configuration.favicon_url,
        sizes: "512x512",
        type: "image/png",
      },
    ],
  };

  return new Response(JSON.stringify(manifest, null, 2), {
    headers: {
      "Content-Type": "application/manifest+json",
    },
  });
};
