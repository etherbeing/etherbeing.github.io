<script lang="ts">
    export const { children } = $props();
</script>

<svelte:head>
    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <title>Skydash Admin</title>
    <!-- plugins:css -->
    <link rel="stylesheet" href="/src/assets/dashboard/vendors/feather/feather.css" />
    <link
        rel="stylesheet"
        href="/src/assets/dashboard/vendors/ti-icons/css/themify-icons.css"
    />
    <link rel="stylesheet" href="/src/assets/dashboard/vendors/css/vendor.bundle.base.css" />
    <!-- endinject -->
    <!-- Plugin css for this page -->
    <!-- End plugin css for this page -->
    <!-- inject:css -->
    <link rel="stylesheet" href="/src/assets/dashboard/css/vertical-layout-light/style.css" />
    <!-- endinject -->
    <link rel="shortcut icon" href="/src/assets/dashboard/images/favicon.png" />

    <!-- container-scroller -->
    <!-- plugins:js -->
    <script src="/src/assets/dashboard/vendors/js/vendor.bundle.base.js"></script>
    <!-- endinject -->
    <!-- Plugin js for this page -->
    <!-- End plugin js for this page -->
    <!-- inject:js -->
    <script src="/src/assets/dashboard/js/off-canvas.js"></script>
    <script src="/src/assets/dashboard/js/hoverable-collapse.js"></script>
    <script src="/src/assets/dashboard/js/template.js"></script>
    <script src="/src/assets/dashboard/js/settings.js"></script>
    <script src="/src/assets/dashboard/js/todolist.js"></script>
    <!-- endinject -->
</svelte:head>

{@render children()}
