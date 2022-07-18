<script>
    import { page } from "$app/stores";

    import "../app.css";
    import Header from "$lib/header.svelte";
</script>

<header>
    <Header />
</header>
{#if $page.url.pathname.includes("/dashboard/servers")}
    <slot />
{:else}
    <main>
        <slot />
    </main>
{/if}
