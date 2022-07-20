<script lang="ts">
    interface Option {
        color?: string;
        selected?: boolean;
        name: string;
        id: string;
    }

    export let title: string;
    export let id: string;
    export let options: Option[] = [];
    export let to: any = null;
    export let onchange: any = null;

    const colorUpdateAndOnChange = async (e: Event) => {
        const target = e.target as HTMLSelectElement;
        const option = options.find(
            (x) => x.id == target.selectedOptions[0].id
        ) as Option;

        target.style.color = "";

        if (option.color) {
            target.style.color = option.color;
        }

        if (onchange) {
            onchange(e);
        }
    };
</script>

<label for={id} class="px-0 block text-gray-300">
    {title}
</label>
<select
    {id}
    bind:this={to}
    on:change={colorUpdateAndOnChange}
    class="bg-gray-50 border border-gray-300 rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 placeholder-gray-400 text-white focus:border-blue-500"
>
    <option disabled selected>Select a {title}</option>
    {#each options as option}
        <option selected={option.selected || false} id={option.id}>
            {option.name}
        </option>
    {/each}
</select>
