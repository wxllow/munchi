<script type="ts">
    import { getConfig } from "$lib/config";
    import axios from "axios";
    import { onMount } from "svelte";
    import urlJoin from "url-join";

    import Loader from "$lib/components/loader.svelte";

    export let servers: Array<PartialGuild> = [];

    const loadServers = async () => {
        const resp = await axios.get(
            urlJoin(
                getConfig().backend_uri,
                "/me/guilds",
                "?token=" + localStorage.getItem("token")
            )
        );

        resp.data.map((guild: PartialGuild) => {
            if (guild.can_manage) servers.push(guild);
        });
    };

    onMount(() => {
        if (!localStorage.getItem("token")) {
            window.location.href = "/";
        }

        loadServers()
            .then(() => {
                servers = servers.sort((a, b) => {
                    return Number(b.has_munchi) - Number(a.has_munchi);
                }); // Update servers in the page and sort by whether the server has munchi
            })
            .catch(console.error);
    });
</script>

<div class="text-center justify-center">
    <h1 class="text-5xl">Select a server</h1>
    {#if servers.length > 0}
        <div
            class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-5"
        >
            {#each servers as server}
                <div class={server.has_munchi ? "" : "brightness-50"}>
                    <div class="rounded overflow-hidden hover:brightness-90">
                        <a
                            href={server.has_munchi
                                ? `/dashboard/servers/${server.id}`
                                : `https://discord.com/api/oauth2/authorize?client_id=${
                                      getConfig().application_id
                                  }&permissions=8&scope=bot%20applications.commands&guild_id=${
                                      server.id
                                  }`}
                        >
                            <img
                                class="w-24 rounded-2xl"
                                alt={`Server icon`}
                                src={server.icon_url || "/defaults/clyde.png"}
                            />
                            <p class="text-2xl">
                                {server.name}
                            </p>
                        </a>
                    </div>
                </div>
            {/each}
        </div>
    {:else}
        <Loader />
    {/if}
</div>
