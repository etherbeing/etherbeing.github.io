<script lang="ts">
  // import { _ } from "svelte-i18n";
  // import { isLoading } from "svelte-i18n";
  // import { QueryClientProvider } from "@tanstack/svelte-query";
  // import { baseQuery } from "./services/http/rest/RestSetup";
  import { client } from "./services/http/graphql";
  import { setContextClient } from "@urql/svelte";
  import BaseRoutes from "./routes/BaseRoutes.svelte";
  import { onMount, setContext } from "svelte";
  import { writable, type Writable } from "svelte/store";
  import { REFRESH_RATE, REFRESH_UNFOLD_CONTEXT_NAME } from "./consts";

  setContextClient(client);
  document.title = "etherbeing";
  let theme: Writable<"light" | "dark"> = writable(
    (localStorage.getItem("theme") as "light" | "dark") || "dark",
  );
  // let theme: "light" | "dark" = $state("dark");
  setContext("theme", theme);

  let pendingRefresh = $state(false);

  const refreshUnfold: Writable<() => void> = writable(() => {
    pendingRefresh = true;
  }); // makes available right away a function to refresh the page

  setContext(REFRESH_UNFOLD_CONTEXT_NAME, refreshUnfold);

  theme.subscribe((th) => {
    localStorage.setItem("theme", th);
    $refreshUnfold();
  });

  const refreshUnfoldCallback = () => {
    requestAnimationFrame(() => {
      // FIXME the theme isn't changing the image but without this the performance degrade as hell
      startLoader();
      // @ts-expect-error Works along with the JS implementation, this makes it actually re-render jarallax images when needed
      window.jarallax(document.querySelectorAll(".jarallax"), "destroy");
      // @ts-expect-error now the app can refresh unfold quickly and easily
      window.startUp();
    });
  };

  onMount(() => {
    const lens = setInterval(() => {
      // @ts-expect-error Actions to be declared to expose it to the Svelte application
      if (window.startUp) {
        refreshUnfold.set(refreshUnfoldCallback);
        if (pendingRefresh) {
          // if the user called the function when not ready yet
          refreshUnfoldCallback();
          pendingRefresh = false;
        }
        clearInterval(lens);
      }
    }, REFRESH_RATE); // perhaps this is too much
  });

  const SITE_LOADER_WRAP = document.querySelectorAll(".site-loader-wrap");
  const OVERLAYER = document.querySelectorAll("#unslate_co--overlayer");

  const startLoader = () => {
    SITE_LOADER_WRAP.forEach((el) => el.setAttribute("style", ""));
    OVERLAYER.forEach((el) => el.setAttribute("style", ""));
  };
</script>

<BaseRoutes></BaseRoutes>
