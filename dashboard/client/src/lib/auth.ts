import urlJoin from "url-join";
import { getConfig } from "$lib/config";

const config = getConfig();

export const login = async () => {
    window.location.href = `https://discord.com/api/oauth2/authorize?client_id=${
        config.application_id
    }&redirect_uri=${encodeURIComponent(
        urlJoin(config.client_uri, "/callback")
    )}&response_type=code&scope=identify%20guilds`;
}
