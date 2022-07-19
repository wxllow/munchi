<script>
    import { getConfig } from "$lib/config";
</script>

<div
    class="py-16 md:py-48"
    style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%)"
>
    <div class="container mx-auto px-6">
        <h1 class="text-6xl font-extrabold">Munchi &lt;3</h1>
        <p>
            Free, fast, powerful, and open-source replacement for all your
            Discord server's needs.
        </p>
        <a
            class="rounded-lg bg-sky-500 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
            href={`https://discord.com/api/oauth2/authorize?client_id=${
                getConfig().application_id
            }&permissions=8&scope=bot%20applications.commands`}
        >
            Add to Discord
        </a>
        <a
            class="inline-flex rounded-lg bg-gray-800 px-5 py-2.5 mr-2 mb-2 hover:brightness-90"
            href="https://github.com/wxllow/munchi"
        >
            View on Github
        </a>
    </div>
</div>
