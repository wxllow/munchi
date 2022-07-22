<script lang="ts">
    interface Option {
        color?: string;
        selected?: boolean;
        name: string;
        id: string;
    }

    export let label: string | null = null;
    export let title: string;
    export let id: string;
    export let options: Option[] = [];
    export let to: any = null;
    export let onchange: any = null;
    export let multiple: boolean = false;
</script>

<label for={id} class="px-0 block text-gray-300">
    {label || title}
</label>
<select
    {id}
    {multiple}
    bind:this={to}
    on:change={onchange}
    class="bg-gray-50 border border-gray-300 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
>
    <option disabled selected>Select a {title}</option>
    {#each options as option}
        <option
            selected={option.selected || false}
            id={option.id}
            style={`color: ${option.color}`}
        >
            {option.name}
        </option>
    {/each}
</select>
