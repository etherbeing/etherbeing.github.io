<script>
    import { link } from "svelte-spa-router";
</script>

<footer class="unslate_co--footer unslate_co--section">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-7">
                <div class="footer-site-logo">
                    <a use:link href="/">etherbeing<span>.</span></a>
                </div>

                <ul class="footer-site-social">
                    <li><a href="#">Facebook</a></li>
                    <li><a href="#">Twitter</a></li>
                    <li><a href="#">Instagram</a></li>
                    <li><a href="#">Dribbble</a></li>
                    <li><a href="#">Behance</a></li>
                </ul>

                <p class="site-copyright">
                    <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
                    Copyright &copy;
                    {new Date().getFullYear()}
                    All rights reserved | This template is designed with
                    <i class="icon-heart" aria-hidden="true"></i>
                    by
                    <a href="https://colorlib.com" target="_blank">Colorlib</a>
                    and developed by Esteban Chacon. See more in
                    <a use:link href="/copyright">here</a>
                    <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
                </p>
            </div>
        </div>
    </div>
</footer>
