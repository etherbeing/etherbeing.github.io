<script lang="ts">
    import Footer from "../../../lib/dashboard/Footer.svelte";
    import Header from "../../../lib/dashboard/Header.svelte";
    import RightSidebar from "../../../lib/dashboard/RightSidebar.svelte";
    import SettingsPanel from "../../../lib/dashboard/SettingsPanel.svelte";
    import Sidebar from "../../../lib/dashboard/Sidebar.svelte";

    import "/src/assets/dashboard/vendors/feather/feather.css";

    import "/src/assets/dashboard/vendors/ti-icons/css/themify-icons.css";

    import "/src/assets/dashboard/vendors/css/vendor.bundle.base.css";

    import "/src/assets/dashboard/vendors/datatables.net-bs4/dataTables.bootstrap4.css";

    import "/src/assets/dashboard/vendors/ti-icons/css/themify-icons.css";
    import "/src/assets/dashboard/js/select.dataTables.min.css";

    import "/src/assets/dashboard/css/vertical-layout-light/style.css";

    const { children } = $props();
</script>

<svelte:head>
    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <title>Skydash Admin</title>
    <link rel="shortcut icon" href="/src/assets/dashboard/images/favicon.png" />

    <!-- plugins:js -->
    <script
        defer
        async={false}
        src="/src/assets/dashboard/vendors/js/vendor.bundle.base.js"
    ></script>
    <!-- endinject -->
    <!-- Plugin js for this page -->
    <script
        defer
        async={false}
        src="/src/assets/dashboard/vendors/chart.js/Chart.min.js"
    ></script>
    <script
        defer
        async={false}
        src="/src/assets/dashboard/vendors/datatables.net/jquery.dataTables.js"
    ></script>
    <script
        defer
        async={false}
        src="/src/assets/dashboard/vendors/datatables.net-bs4/dataTables.bootstrap4.js"
    ></script>
    <script
        defer
        async={false}
        src="/src/assets/dashboard/js/dataTables.select.min.js"
    ></script>

    <!-- End plugin js for this page -->
    <!-- inject:js -->
    <script
        defer
        async={false}
        src="/src/assets/dashboard/js/off-canvas.js"
    ></script>
    <script
        defer
        async={false}
        src="/src/assets/dashboard/js/hoverable-collapse.js"
    ></script>
    <script
        defer
        async={false}
        src="/src/assets/dashboard/js/template.js"
    ></script>
    <script
        defer
        async={false}
        src="/src/assets/dashboard/js/settings.js"
    ></script>
    <script
        defer
        async={false}
        src="/src/assets/dashboard/js/todolist.js"
    ></script>
    <!-- endinject -->
    <!-- Custom js for this page-->
    <script
        defer
        async={false}
        src="/src/assets/dashboard/js/dashboard.js"
    ></script>
    <script
        defer
        async={false}
        src="/src/assets/dashboard/js/Chart.roundedBarCharts.js"
    ></script>
</svelte:head>

<div class="container-scroller">
    <Header></Header>
    <div class="container-fluid page-body-wrapper">
        <SettingsPanel></SettingsPanel>
        <RightSidebar></RightSidebar>
        <!-- partial -->
        <Sidebar></Sidebar>
        <!-- partial -->
        <div class="main-panel">
            <div class="content-wrapper">
                {@render children()}
            </div>
            <!-- content-wrapper ends -->
            <Footer></Footer>
        </div>
        <!-- main-panel ends -->
    </div>
    <!-- page-body-wrapper ends -->
</div>
