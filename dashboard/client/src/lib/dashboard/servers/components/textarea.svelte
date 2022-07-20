<script lang="ts">
    export let title: string;
    export let id: string;
    export let placeholder: string | null = null;
    export let value: any | null = null;
    export let to: any = null;
    export let type: string | null = null;
    export let onchange: any = null;
</script>

<label for={id} class="px-0 block text-gray-300">
    {title}
</label>
<textarea
    {id}
    bind:this={to}
    type={type || "text"}
    on:change={onchange}
    value={value || ""}
    placeholder={placeholder || title}
    class="bg-gray-50 border border-gray-300 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
/>
