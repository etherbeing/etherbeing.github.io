<script lang="ts">
  // import { _ } from "svelte-i18n";
  // import { isLoading } from "svelte-i18n";
  // import { QueryClientProvider } from "@tanstack/svelte-query";
  // import { baseQuery } from "./services/http/rest/RestSetup";
  import { client } from "./services/http/graphql";
  import { setContextClient } from "@urql/svelte";
  import Header from "./lib/Header.svelte";
  import Footer from "./lib/Footer.svelte";
  import Routes from "./routes/Routes.svelte";
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
    requestAnimationFrame(() => { // FIXME the theme isn't changing the image but without this the performance degrade as hell
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

<svelte:head>
  {#if $theme === "dark"}
    <link
      rel="stylesheet"
      href="/src/assets/dark/css/vendor/icomoon/style.css"
    />
    <link
      rel="stylesheet"
      href="/src/assets/dark/css/vendor/owl.carousel.min.css"
    />
    <link rel="stylesheet" href="/src/assets/dark/css/vendor/animate.min.css" />
    <link rel="stylesheet" href="/src/assets/dark/css/vendor/aos.css" />
    <link
      rel="stylesheet"
      href="/src/assets/dark/css/vendor/bootstrap.min.css"
    />
    <link
      rel="stylesheet"
      href="/src/assets/dark/css/vendor/jquery.fancybox.min.css"
    />
    <link rel="stylesheet" href="/src/assets/dark/css/style.css" />

    <!-- Async false is pretty important below as for some reason my current chrome version is loading both those scripts asynchronous -->
    <script
      defer
      async={false}
      src="/src/assets/dark/js/scripts-dist.js"
    ></script>
    <script defer async={false} src="/src/assets/dark/js/main.js"></script>
  {/if}
  {#if $theme === "light"}
    <link
      rel="stylesheet"
      href="/src/assets/light/css/vendor/icomoon/style.css"
    />
    <link
      rel="stylesheet"
      href="/src/assets/light/css/vendor/owl.carousel.min.css"
    />
    <link
      rel="stylesheet"
      href="/src/assets/light/css/vendor/animate.min.css"
    />
    <link rel="stylesheet" href="/src/assets/light/css/vendor/aos.css" />
    <link
      rel="stylesheet"
      href="/src/assets/light/css/vendor/bootstrap.min.css"
    />
    <link
      rel="stylesheet"
      href="/src/assets/light/css/vendor/jquery.fancybox.min.css"
    />

    <!-- Theme Style -->
    <link rel="stylesheet" href="/src/assets/light/css/style.css" />

    <!-- Async false is pretty important below as for some reason my current chrome version is loading both those scripts asynchronous -->
    <script
      defer
      async={false}
      src="/src/assets/light/js/scripts-dist.js"
    ></script>
    <script defer async={false} src="/src/assets/light/js/main.js"></script>
  {/if}
</svelte:head>

<div class="unslate_co--site-wrap">
  <div class="unslate_co--site-inner">
    <div class="lines-wrap">
      <div class="lines-inner">
        <div class="lines"></div>
      </div>
    </div>
    <!-- END lines -->

    <Header></Header>
    <!-- END nav -->
    <Routes></Routes>
  </div>
  <!-- END .unslate_co-site-inner -->
  <Footer></Footer>
  <!-- <QueryClientProvider client={baseQuery}>
    {#if $isLoading}
      Please wait...
    {:else}
    {/if}
  </QueryClientProvider> -->
</div>
