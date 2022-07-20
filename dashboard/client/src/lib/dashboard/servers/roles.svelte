<script lang="ts">
    import { page } from "$app/stores";
    import axios from "axios";
    import urlJoin from "url-join";
    import { getConfig } from "$lib/config";

    import Dropdown from "$lib/dashboard/servers/components/dropdown.svelte";
    import Input from "$lib/dashboard/servers/components/input.svelte";

    export let server: Guild;
    let addModalMessageElem: HTMLInputElement;
    let addModalEmojiElem: HTMLInputElement;
    let addModalTypeElem: HTMLSelectElement;
    let addModalRoleElem: HTMLSelectElement;

    const toggleAddModal = (e: Event) => {
        document.getElementById("addModal")?.classList.toggle("hidden");
    };

    const validateField = (i: any): boolean => {
        if (!i || i.value === "" || i.value === 0) {
            return false;
        }

        return true;
    };

    const submitAddModal = async (e: Event) => {
        let message = addModalMessageElem.value;
        let emoji = addModalEmojiElem.value;
        let type = addModalTypeElem.selectedOptions[0].id;
        let role = addModalRoleElem.selectedOptions[0].id;

        if (
            !validateField(message) ||
            !validateField(emoji) ||
            !validateField(type) ||
            !validateField(role)
        ) {
            return alert("Please fill out all fields!");
        }

        const key = (e.target as HTMLInputElement | HTMLTextAreaElement).id;
        const value = (e.target as HTMLInputElement | HTMLTextAreaElement)
            .value;

        let resp = await axios.post(
            urlJoin(
                getConfig().backend_uri,
                `/guilds/${$page.params.slug}/add_reaction_role`,
                "?token=" + localStorage.getItem("token")
            ),
            {
                message,
                emoji,
                type,
                role,
            }
        );
    };
</script>

<h2 class="text-6xl font-bold text-center">Reaction Roles</h2>
<ul>
    <h3 class="text-4xl">Messages</h3>
    {#each server.reaction_roles_message as message}
        <li class="pl-12">
            <h4 class="p-0 text-2xl">
                {message.message} (Type: {message.type})
            </h4>
            <ul>
                {#each Object.keys(message.roles) as reaction}
                    <li>
                        <h5 class="text-1xl">{reaction}:</h5>
                        <ul class="list-disc px-8">
                            {#each message.roles[reaction] as role}
                                <li class="p-0">
                                    <span
                                        class="p-0"
                                        style={`color: #${parseInt(
                                            server.roles.find(
                                                (x) => x.id == role
                                            ).color
                                        ).toString(16)}`}
                                    >
                                        {server.roles.find((x) => x.id == role)
                                            .name}
                                    </span>
                                </li>
                            {/each}
                        </ul>
                    </li>
                {/each}
            </ul>
        </li>
    {/each}
</ul>
<div class="text-center">
    <button
        class="rounded-lg bg-sky-500 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
        on:click={toggleAddModal}
    >
        Add Message or Reaction
    </button>
</div>

<!-- Add message modal -->
<div
    id="addModal"
    tabindex="-1"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50
    w-full md:inset-0 h-modal md:h-full"
>
    <div
        class="relative p-4 w-full max-w-2xl h-full md:h-auto bg-white rounded-lg shadow dark:bg-gray-700"
    >
        <h1 class="my-0 px-0 text-3xl font-semibold">
            <button class="font-bold" on:click={toggleAddModal}>&lt;</button>
            Add Message/Reaction
        </h1>

        <Input
            bind:to={addModalMessageElem}
            title="Message ID"
            id="message_id"
        />
        <Input bind:to={addModalEmojiElem} title="Emoji" id="emoji" />
        <Dropdown
            bind:to={addModalTypeElem}
            title="Type"
            id="type"
            options={[
                { name: "normal", id: "normal" },
                { name: "verify", id: "verify" },
            ]}
        />
        <Dropdown
            bind:to={addModalRoleElem}
            title="Role"
            id="role"
            options={server.roles
                .sort((a, b) => a.position - b.position)
                .reverse()
                .map((role) => ({
                    name: role.name,
                    id: role.id,
                    color: `#${parseInt(role.color).toString(16)}`,
                }))}
        />
        <button
            class="rounded-lg bg-green-400 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
            on:click={submitAddModal}
        >
            Add
        </button>
    </div>
</div>
