<script lang="ts">
    import { saveChanges, saveObjectChanges } from "$lib/dashboard/dashboard";
    import { page } from "$app/stores";

    import Textarea from "$lib/dashboard/servers/components/textarea.svelte";
    import Input from "$lib/dashboard/servers/components/input.svelte";

    export let server: Guild;

    const saveChange = async (e: Event) => {
        await saveChanges(e, $page.params.slug).catch(console.error);
    };

    const saveObjectChange = async (e: Event) => {
        await saveObjectChanges(e, $page.params.slug).catch(console.error);
    };
</script>

<h2 class="text-6xl font-bold text-center">Welcome</h2>
<div>
    <div class="border-b pb-5">
        <Input
            title="Welcome Channel"
            id="welcome_channel"
            placeholder="Channel ID"
            value={server.welcome_channel}
            onchange={saveChange}
        />
        <Textarea
            title="Welcome Message"
            id="welcome_message"
            value={server.welcome_message}
            onchange={saveChange}
        />
        <p class="text-2xl text-center">and/or</p>
        <Input
            title="Welcome Embed Title"
            id="welcome_embed.title"
            placeholder="Channel ID"
            value={server.welcome_embed.title}
            onchange={saveObjectChange}
        />
        <Textarea
            title="Welcome Embed Description"
            id="welcome_embed.description"
            value={server.welcome_embed.description}
            onchange={saveObjectChange}
        />
    </div>
    <div class="py-5">
        <Input
            title="Goodbye Channel"
            id="goodbye_channel"
            placeholder="Channel ID"
            value={server.goodbye_channel}
            onchange={saveChange}
        />
        <Textarea
            title="Goodbye Message"
            id="goodbye_message"
            value={server.goodbye_message}
            onchange={saveChange}
        />
        <p class="text-2xl text-center">and/or</p>
        <Input
            title="Goodbye Embed Title"
            id="goodbye_embed.title"
            placeholder="Channel ID"
            value={server.goodbye_embed.title}
            onchange={saveObjectChange}
        />
        <Textarea
            title="Goodbye Embed Description"
            id="goodbye_embed.description"
            value={server.goodbye_embed.description}
            onchange={saveObjectChange}
        />
    </div>
    <p class="text-2xl font-bold">Variables</p>
    <ul>
        <li>
            <span class="font-bold">{"{server}"}</span> The server name
        </li>
        <li>
            <span class="font-bold">{"{user}"}</span>The user's display name
        </li>
        <li>
            <span class="font-bold">{"{user_mention}"}</span>Mentions the user
        </li>
    </ul>
</div>
