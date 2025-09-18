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
                    <li><a href="#">Twitter (X)</a></li>
                    <li><a href="#">Telegram</a></li>
                    <li><a href="#">LinkedIn</a></li>
                    <li><a href="#">Reddit</a></li>
                    <li><a target="_blank" href={"https://instagram.com/real_etherbeing"}>Instagram</a></li>
                    <li><a target="_blank" href={"https://wa.me/+46764039298"}>Whatsapp</a></li>
                    <li><a target="_blank" href={"https://discord.gg/k9qhhmpk"}>Discord</a></li>
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
