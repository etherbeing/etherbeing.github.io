<script lang="ts">
    import { link } from "svelte-spa-router";
</script>

<!-- partial:partials/_sidebar.html -->
<nav class="sidebar sidebar-offcanvas" id="sidebar">
    <ul class="nav">
        <li class="nav-item">
            <a class="nav-link" use:link href="/admin/dashboard/">
                <i class="icon-grid menu-icon"></i>
                <span class="menu-title">Dashboard</span>
            </a>
        </li>
        <li class="nav-item">
            <a
                class="nav-link"
                data-toggle="collapse"
                href="#ui-basic"
                aria-expanded="false"
                aria-controls="ui-basic"
            >
                <i class="icon-layout menu-icon"></i>
                <span class="menu-title">UI Elements</span>
                <i class="menu-arrow"></i>
            </a>
            <div class="collapse" id="ui-basic">
                <ul class="nav flex-column sub-menu">
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/admin/buttons/"
                            >Buttons</a
                        >
                    </li>
                    <li class="nav-item">
                        <a use:link
                            class="nav-link"
                            href="/admin/dropdowns/">Dropdowns</a
                        >
                    </li>
                    <li class="nav-item">
                        <a use:link
                            class="nav-link"
                            href="/admin/typography"
                            >Typography</a
                        >
                    </li>
                </ul>
            </div>
        </li>
        <li class="nav-item">
            <a
                class="nav-link"
                data-toggle="collapse"
                href="#form-elements"
                aria-expanded="false"
                aria-controls="form-elements"
            >
                <i class="icon-columns menu-icon"></i>
                <span class="menu-title">Form elements</span>
                <i class="menu-arrow"></i>
            </a>
            <div class="collapse" id="form-elements">
                <ul class="nav flex-column sub-menu">
                    <li class="nav-item">
                        <a use:link
                            class="nav-link"
                            href="/admin/basic_elements/"
                            >Basic Elements</a
                        >
                    </li>
                </ul>
            </div>
        </li>
        <li class="nav-item">
            <a
                class="nav-link"
                data-toggle="collapse"
                href="#charts"
                aria-expanded="false"
                aria-controls="charts"
            >
                <i class="icon-bar-graph menu-icon"></i>
                <span class="menu-title">Charts</span>
                <i class="menu-arrow"></i>
            </a>
            <div class="collapse" id="charts">
                <ul class="nav flex-column sub-menu">
                    <li class="nav-item">
                        <a class="nav-link" use:link href="/admin/chartjs/"
                            >ChartJs</a
                        >
                    </li>
                </ul>
            </div>
        </li>
        <li class="nav-item">
            <a
                class="nav-link"
                data-toggle="collapse"
                href="#tables"
                aria-expanded="false"
                aria-controls="tables"
            >
                <i class="icon-grid-2 menu-icon"></i>
                <span class="menu-title">Tables</span>
                <i class="menu-arrow"></i>
            </a>
            <div class="collapse" id="tables">
                <ul class="nav flex-column sub-menu">
                    <li class="nav-item">
                        <a class="nav-link" use:link href="/admin/basic-table/"
                            >Basic table</a
                        >
                    </li>
                </ul>
            </div>
        </li>
        <li class="nav-item">
            <a
                class="nav-link"
                data-toggle="collapse"
                href="#icons"
                aria-expanded="false"
                aria-controls="icons"
            >
                <i class="icon-contract menu-icon"></i>
                <span class="menu-title">Icons</span>
                <i class="menu-arrow"></i>
            </a>
            <div class="collapse" id="icons">
                <ul class="nav flex-column sub-menu">
                    <li class="nav-item">
                        <a class="nav-link" use:link href="/admin/mdi/"
                            >Mdi icons</a
                        >
                    </li>
                </ul>
            </div>
        </li>
    </ul>
</nav>
