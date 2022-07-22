<script lang="ts">
    import { page } from "$app/stores";
    import axios from "axios";
    import urlJoin from "url-join";
    import { getConfig } from "$lib/config";
    import Dropdown from "$lib/dashboard/servers/components/dropdown.svelte";
    import Input from "$lib/dashboard/servers/components/input.svelte";

    // Data from parent component (dashboard/servers/[slug].svelte)

    export let server: Guild;

    // Elements
    let addModalForm: HTMLFormElement;
    let addModalChannelElem: HTMLSelectElement;
    let addModalMessageElem: HTMLInputElement;
    let addModalTypeElem: HTMLSelectElement;
    let addModalEmojiRoleElems: HTMLDivElement;

    // Refetch Server
    const reloadServer = async () => {
        window.location.reload();
    };

    // Validate a field
    const validateField = async (i: any): Promise<boolean> => {
        if (!i || i.value === "" || i.value === 0) {
            return false;
        }

        return true;
    };

    // Add Modal
    const toggleAddModal = async (e?: Event) => {
        document.getElementById("addModal")?.classList.toggle("hidden");

        addModalForm.reset();

        // Remove all extra role nodes
        addModalEmojiRoleElems.querySelectorAll("#cloneme").forEach((e) => {
            if (addModalEmojiRoleElems.querySelectorAll("#cloneme").length < 2)
                return;

            addModalEmojiRoleElems.removeChild(e);
        });
    };

    // Duplicating the reaction elements (for adding multiple reactions)
    const clone = async () => {
        const elem = addModalEmojiRoleElems.querySelector(
            "#cloneme"
        ) as HTMLDivElement;

        addModalEmojiRoleElems.appendChild(elem.cloneNode(true));
    };

    // Edit an existing message
    const editMessage = async (msg: {
        message: string;
        type: string;
        channel?: string;
        roles: {
            [key: string]: string[];
        };
    }) => {
        await toggleAddModal();

        if (msg.channel)
            (
                addModalChannelElem.querySelector(
                    `option[id='${msg.channel}']`
                ) as HTMLOptionElement
            ).selected = true;

        addModalMessageElem.value = msg.message;
        (
            addModalTypeElem.querySelector(`#${msg.type}`) as HTMLOptionElement
        ).selected = true;

        while (
            addModalEmojiRoleElems.querySelectorAll("#cloneme").length <
            Object.keys(msg.roles).length
        ) {
            await clone();
        }

        let i = 0;

        Object.keys(msg.roles).forEach((key, i) => {
            const elem = addModalEmojiRoleElems.querySelectorAll("#cloneme")[i];

            const selectElem = elem.querySelector(
                "select"
            ) as HTMLSelectElement;

            (elem.querySelector("#emoji") as HTMLInputElement).value = key;

            msg.roles[key].forEach((role) => {
                const optionElem = selectElem.querySelector(
                    `option[id='${role}']`
                ) as HTMLOptionElement;

                optionElem.selected = true;
            });

            i++;
        });
    };

    // Submit the add modal
    const submitAddModal = async (e?: Event) => {
        let message = addModalMessageElem.value;
        let type = addModalTypeElem.selectedOptions[0].id;
        let channel = addModalChannelElem.selectedOptions[0].id;

        const reactionEmojis = Array.from(
            addModalEmojiRoleElems.querySelectorAll("#emoji")
        ) as HTMLInputElement[];
        const roles = Array.from(
            addModalEmojiRoleElems.querySelectorAll("#role")
        ) as HTMLSelectElement[];

        const reactions = Object.fromEntries(
            reactionEmojis.map((e, i) => {
                return [
                    e.value,
                    Array.from(roles[i].selectedOptions).map((r) => r.id),
                ];
            })
        );

        if (
            !validateField(message) ||
            !validateField(type) ||
            !validateField(reactions)
        ) {
            return alert("Please fill out all fields!");
        }

        await axios
            .post(
                urlJoin(
                    getConfig().backend_uri,
                    `/guilds/${$page.params.slug}/add_reaction_message`,
                    "?token=" + localStorage.getItem("token")
                ),
                {
                    channel,
                    message,
                    type,
                    roles: reactions,
                }
            )
            .then(reloadServer)
            .catch((err) => {
                console.error(err);
                alert(
                    `Something went wrong! Backend returned ${err.response.status} status`
                );
            });
    };

    const deleteMessage = async (e: Event) => {
        let message = (e.target as HTMLButtonElement).id;

        await axios
            .delete(
                urlJoin(
                    getConfig().backend_uri,
                    `/guilds/${$page.params.slug}/remove_reaction_message/${message}`,
                    "?token=" + localStorage.getItem("token")
                )
            )
            .then(reloadServer);
    };
</script>

<h2 class="text-6xl font-bold text-center">Reaction Roles</h2>
<h3 class="text-4xl">Messages</h3>
<div class="overflow-x-auto relative">
    <table class="w-full text-sm text-left">
        <thead
            class="text-xs  uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
        >
            <tr>
                <th scope="col" class="py-3 px-6"> Channel </th>
                <th scope="col" class="py-3 px-6"> Message ID </th>
                <th scope="col" class="py-3 px-6"> Type </th>
                <th scope="col" class="py-3 px-6"> Roles </th>
                <th scope="col" class="py-3 px-6"> Actions </th>
            </tr>
        </thead>
        <tbody>
            {#each server.reaction_roles_message as message}
                <tr
                    class="bg-white border-b dark:bg-gray-800 dark:border-gray-700"
                    id={message.message}
                >
                    <td class="py-4 px-6">
                        #{message.channel
                            ? server.channels.find(
                                  (x) => x.id == message.channel && x.type == 0
                              ).name
                            : "Unknown"}
                    </td>
                    <td class="py-4 px-6"> {message.message} </td>
                    <td class="py-4 px-6">
                        {message.type.charAt(0).toUpperCase() +
                            message.type.slice(1)}
                    </td>
                    <td class="py-4 px-6">
                        {#each Object.keys(message.roles) as reaction}
                            {#each message.roles[reaction] as role}
                                {#if server.roles.find((x) => x.id == role)}
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
                                {:else}
                                    <span class="p-0 text-gray-200"
                                        >Unknown role</span
                                    >
                                {/if}
                            {/each}
                        {/each}
                    </td>
                    <td class="px-6">
                        <button
                            class="rounded-lg bg-gray-600 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
                            on:click={() => editMessage(message)}
                            id={message.message}
                        >
                            Edit
                        </button>
                        <button
                            class="rounded-lg bg-red-500 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
                            on:click={deleteMessage}
                            id={message.message}
                        >
                            Remove
                        </button>
                    </td>
                </tr>
            {/each}
            {#if server.reaction_roles_message.length < 1}
                <h1>No messages yet, add some!</h1>
            {/if}
        </tbody>
    </table>
</div>

<div class="text-center">
    <button
        data-tooltip-target="tooltip-comingsoon"
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
        <h1 class="my-0 px-0 text-3xl font-semibold">Add Message/Reaction</h1>
        <form bind:this={addModalForm}>
            <Dropdown
                bind:to={addModalChannelElem}
                title="Channel"
                id="channel"
                options={server.channels
                    .filter((x) => x.type == 0)
                    .map((x) => ({
                        id: x.id,
                        name: `#${x.name}`,
                    }))}
            />
            <Input
                bind:to={addModalMessageElem}
                title="Message ID"
                id="message_id"
            />
            <Dropdown
                bind:to={addModalTypeElem}
                title="Type"
                id="type"
                options={[
                    { name: "normal", id: "normal" },
                    { name: "verify", id: "verify" },
                ]}
            />
            <h1 class="px-0 text-2xl">Reactions</h1>
            <div class="p-0" bind:this={addModalEmojiRoleElems}>
                <div class="p-0" id="cloneme">
                    <Input id="emoji" title="Emoji" />
                    <Dropdown
                        multiple={true}
                        label="Roles"
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
                </div>
                <button
                    class="rounded-lg bg-green-400 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
                    on:click={clone}
                >
                    Add Another Reaction
                </button>
            </div>

            <button
                class="rounded-lg bg-green-400 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
                on:click={submitAddModal}
            >
                Add
            </button>
            <button
                class="rounded-lg bg-gray-400 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
                on:click={toggleAddModal}
            >
                Cancel
            </button>
        </form>
    </div>
</div>

<style>
</style>
