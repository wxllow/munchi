<script type="ts">
    import { page } from "$app/stores";
    import axios from "axios";
    import urlJoin from "url-join";
    import { getConfig } from "$lib/config";
    import { onMount } from "svelte";

    const login = async () => {
        axios
            .get(
                urlJoin(
                    getConfig().backend_uri,
                    `/oauth/callback?code=${$page.url.searchParams.get("code")}`
                )
            )
            .then((resp) => {
                localStorage.setItem("token", resp.data.token);
                window.location.href = "/dashboard";
            })
            .catch((err) => {
                console.error(err);
                return alert("Login failed!");
            });
    };

    onMount(() => {
        login();
    });
</script>
