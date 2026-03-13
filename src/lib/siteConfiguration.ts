export type SiteConfiguration = {
  site_name: string;
  short_name: string;
  site_description: string;
  favicon_url: string;
  theme_color: string;
  background_color: string;
};

export const defaultSiteConfiguration: SiteConfiguration = {
  site_name: "etherbeing",
  short_name: "etherbeing",
  site_description:
    "Cybersecurity, Rust engineering, biological neural networks, and research.",
  favicon_url: "/favicon.png",
  theme_color: "#020617",
  background_color: "#020617",
};

export async function fetchSiteConfiguration(apiUrl?: string): Promise<SiteConfiguration> {
  if (!apiUrl) {
    return defaultSiteConfiguration;
  }

  try {
    const response = await fetch(`${apiUrl}/api/site/configuration/`);
    if (!response.ok) {
      throw new Error("Configuration request failed");
    }
    const payload = (await response.json()) as Partial<SiteConfiguration>;
    return {
      ...defaultSiteConfiguration,
      ...payload,
    };
  } catch {
    return defaultSiteConfiguration;
  }
}
