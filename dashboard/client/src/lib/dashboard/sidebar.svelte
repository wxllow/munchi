<script lang="ts">
    import { page } from "$app/stores";
    import urlJoin from "url-join";

    interface Link {
        name: string;
        url: string;
        image?: string;
        vb?: boolean;
        comingSoon?: boolean;
    }

    export let links: Array<Link> = [
        {
            name: "Home",
            url: "#",
            image: `<path xmlns="http://www.w3.org/2000/svg" d="M7 43V17.45l17.1-12.8 17 12.8V43H26.95V28.95h-5.9V43Z"/>`,
        },
        {
            name: "Welcome/Goodbye",
            url: "#welcome",
            image: `<path xmlns="http://www.w3.org/2000/svg" d="M34.65 47.05V43.6q3.7-.05 6.325-2.675T43.65 34.6h3.45q-.05 5.15-3.7 8.8-3.65 3.65-8.75 3.65ZM.95 13.35q0-5.1 3.65-8.75Q8.25.95 13.4.9v3.45q-3.7.05-6.325 2.675T4.4 13.35Zm5.3 28.35q-2.75-2.75-4.1-6.175Q.8 32.1.8 28.5q0-3.6 1.375-7.05Q3.55 18 6.25 15.3l8.65-8.65q.9-.85 2.075-.875 1.175-.025 2.075.875.95.9.975 2.1.025 1.2-.925 2.05l-7.35 7.4q1.95 2.4 1.825 5.35-.125 2.95-2.125 5l1.3 1.4q2.2-2.25 2.675-5.4.475-3.15-1.225-6.05l15-15q.9-.9 2.075-.9 1.175 0 2.125.9.9.95.9 2.1 0 1.15-.9 2.1L22.65 18.45 24 19.8 37.6 6.2q.9-.9 2.075-.9 1.175 0 2.125.95.9.9.9 2.075 0 1.175-.9 2.075L28.2 24l1.4 1.35L41.05 13.9q.9-.9 2.05-.9t2.05.9q.95.95.95 2.1 0 1.15-.95 2.05L32.35 30.9l1.35 1.4 8.6-8.55q.85-.95 2.05-.925 1.2.025 2.1.925.9.85.9 2.05 0 1.2-.9 2.1L32.7 41.7q-2.8 2.75-6.225 4.125t-7 1.4q-3.575.025-7-1.375T6.25 41.7Z"/>`,
        },
        {
            name: "Moderation",
            url: "#moderation",
            image: `<path d="M24 43.95q-7-1.75-11.5-8.125T8 21.85V9.95l16-6 16 6v11.9q0 7.6-4.5 13.975T24 43.95Z"/>`,
            comingSoon: true,
        },
        {
            name: "Music",
            url: "#music",
            image: `<path xmlns="http://www.w3.org/2000/svg" d="M19.65 42q-3.15 0-5.325-2.175Q12.15 37.65 12.15 34.5q0-3.15 2.175-5.325Q16.5 27 19.65 27q1.4 0 2.525.4t1.975 1.1V6h11.7v6.75h-8.7V34.5q0 3.15-2.175 5.325Q22.8 42 19.65 42Z"/>`,
            comingSoon: true,
        },
        {
            name: "Notifications",
            url: "#notifs",
            image: `<path xmlns="http://www.w3.org/2000/svg" d="M8 38v-3h4.2V19.7q0-4.1 2.475-7.425T21.2 8.1V6.65q0-1.15.825-1.9T24 4q1.15 0 1.975.75.825.75.825 1.9V8.1q4.05.85 6.55 4.175 2.5 3.325 2.5 7.425V35H40v3Zm16 6q-1.6 0-2.8-1.175Q20 41.65 20 40h8q0 1.65-1.175 2.825Q25.65 44 24 44Z"/>`,
            comingSoon: true,
        },
        {
            name: "Voice",
            url: "#vc",
            image: `<path xmlns="http://www.w3.org/2000/svg" d="m40.05 32.75-2.5-2.5q2.4-2.55 3.675-5.225T42.5 18.45q0-3.9-1.275-6.575Q39.95 9.2 37.55 6.65l2.5-2.5q2.8 2.9 4.375 6.325Q46 13.9 46 18.45t-1.575 7.975Q42.85 29.85 40.05 32.75Zm-6.95-7.1-2.5-2.5q.9-1 1.4-2.125.5-1.125.5-2.575 0-1.45-.5-2.575-.5-1.125-1.4-2.125l2.5-2.5q1.3 1.4 2.1 3.275t.8 3.925q0 2.05-.8 3.925t-2.1 3.275Zm-15.1.3q-3.3 0-5.4-2.1-2.1-2.1-2.1-5.4 0-3.3 2.1-5.4 2.1-2.1 5.4-2.1 3.3 0 5.4 2.1 2.1 2.1 2.1 5.4 0 3.3-2.1 5.4-2.1 2.1-5.4 2.1ZM2 42v-4.7q0-1.9.95-3.225Q3.9 32.75 5.4 32q2.55-1.3 6.025-2.15Q14.9 29 18 29t6.55.85q3.45.85 6 2.15 1.5.75 2.475 2.075Q34 35.4 34 37.3V42Z"/>`,
            comingSoon: true,
        },
        {
            name: "Logging",
            url: "#notifs",
            image: `<path xmlns="http://www.w3.org/2000/svg" d="M13.85 34.05H27.6v-3H13.85Zm0-8.55h20.3v-3h-20.3Zm0-8.55h20.3v-3h-20.3ZM9 42q-1.2 0-2.1-.9Q6 40.2 6 39V9q0-1.2.9-2.1Q7.8 6 9 6h30q1.2 0 2.1.9.9.9.9 2.1v30q0 1.2-.9 2.1-.9.9-2.1.9Z"/>`,
            comingSoon: true,
        },
        {
            name: "Extras",
            url: "#extras",
            image: `<path xmlns="http://www.w3.org/2000/svg" d="M38.2 43.95q-.3 0-.55-.075-.25-.075-.5-.325L25.9 32.3v-3.8l2.55-2.55h3.8L43.5 37.2q.25.25.325.5.075.25.075.55 0 .3-.075.55-.075.25-.325.5l-4.25 4.25q-.25.25-.5.325-.25.075-.55.075Zm0-3.55 2.15-2.15-10-10-2.15 2.15ZM9.75 44q-.3 0-.575-.1-.275-.1-.525-.35l-4.2-4.2q-.25-.25-.35-.525-.1-.275-.1-.575 0-.3.1-.55.1-.25.35-.5L15.7 25.95h4.25l1.9-1.9-8.75-8.75h-2.85L4 9.05 8.95 4.1l6.25 6.25v2.85l8.75 8.75 6.5-6.5-3.35-3.35 2.8-2.8h-5.65l-.9-.9 6.4-6.4.9.9v5.65l2.8-2.8 8.45 8.45q.75.75 1.175 1.725.425.975.425 2.075 0 .95-.3 1.875t-.95 1.725L38 17.35l-2.8 2.8-2.6-2.6L22.05 28.1v4.2L10.8 43.55q-.25.25-.5.35-.25.1-.55.1Zm0-3.6 10-10-2.15-2.15-10 10Z"/>`,
            comingSoon: true,
        },
    ];
</script>

<div class="sidebar">
    <aside class="w-64 fixed my-0 h-screen" aria-label="Sidebar">
        <div class="overflow-y-auto py-4 px-3 rounded-lg bg-gray-800">
            <ul class="space-y-2">
                {#each links as link}
                    <li
                        data-tooltip-target={link.comingSoon
                            ? "tooltip-default"
                            : null}
                    >
                        <a
                            href={link.comingSoon ? null : link.url}
                            disabled={link.comingSoon}
                            class="flex items-center p-2 text-base font-normal rounded-lg hover:bg-gray-700 {link.comingSoon
                                ? 'brightness-75 cursor-not-allowed'
                                : ''}"
                        >
                            <svg
                                fill="currentColor"
                                viewBox={`0 0 ${link.vb || 48} ${
                                    link.vb || 48
                                }`}
                                xmlns="http://www.w3.org/2000/svg"
                                class="w-6 h-6 sticky duration-75 text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                                >{@html link.image}</svg
                            >
                            <span class="ml-3">{link.name}</span>
                        </a>
                    </li>
                    <div
                        id="tooltip-default"
                        role="tooltip"
                        class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-gray-700 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                    >
                        Coming soon!
                        <div class="tooltip-arrow" data-popper-arrow />
                    </div>
                {/each}
            </ul>
        </div>
    </aside>
</div>
