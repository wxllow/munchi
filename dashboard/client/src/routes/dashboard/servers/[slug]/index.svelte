<script type="ts">
    import { loadServer } from "$lib/dashboard/dashboard";
    import { page } from "$app/stores";
    import { onMount } from "svelte";

    import Sidebar from "$lib/dashboard/sidebar.svelte";
    import Loader from "$lib/loader.svelte";
    import Welcome from "$lib/dashboard/servers/welcome.svelte";
    import Index from "$lib/dashboard/servers/index.svelte";

    export let server: Guild | null = null;

    onMount(() => {
        if (!localStorage.getItem("token")) {
            window.location.href = "/";
        }

        loadServer($page.params.slug).then((res) => {
            server = res;
        });
    });
</script>

<div>
    <Sidebar />

    {#if server}
        <main class="ml-64 px-2 items-start text-left">
            {#if $page.url.hash === "#welcome"}
                <Welcome {server} />
            {:else}
                <Index {server} />
            {/if}
        </main>
    {:else}
        <div class="ml-66 px-2"><Loader /></div>
    {/if}
</div>
