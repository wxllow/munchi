<script type="ts">
    export let server: Guild;
</script>

<div class="text-center">
    <h2 class="text-6xl font-bold">{server.name}</h2>
    <p>
        {server.approximate_member_count} members | {server.roles.length} roles
    </p>
</div>
<div class="border-t" />
<p>Select a module to continue...</p>
