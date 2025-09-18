<script lang="ts">
    import logo_google from "/src/assets/dark/images/logo-google.png?url";
    import logo_puma from "/src/assets/dark/images/logo-puma.png?url";
    import logo_paypal from "/src/assets/dark/images/logo-paypal.png?url";
    import logo_adobe from "/src/assets/dark/images/logo-adobe.png?url";
    interface Client {
        logo: string;
        name: string;
    }
    let clients: Array<Client> = $state([
        {
            name: "Google",
            logo: logo_google,
        },
        {
            name: "Puma",
            logo: logo_puma,
        },
        {
            name: "PayPal",
            logo: logo_paypal,
        },
        {
            name: "Adobe",
            logo: logo_adobe,
        },
    ]);
</script>

<div class="unslate_co--section">
    <div class="container">
        <div class="owl-carousel logo-slider">
            {#each clients as client}
                <div class="logo-v1 gsap-reveal">
                    <img
                        src={client.logo}
                        alt={client.name}
                        class="img-fluid"
                    />
                </div>
            {/each}
        </div>
    </div>
</div>
