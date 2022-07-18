import axios from "axios";
import urlJoin from "url-join";

import { getConfig } from "$lib/config";



export const loadServer = async (slug: string) => {
    let server: Guild | null = null;

    const resp = await axios.get(
        urlJoin(
            getConfig().backend_uri,
            `/me/guilds/${slug}`,
            "?token=" + localStorage.getItem("token")
        )
    );

    return resp.data;
};

export const saveChanges = async (e: Event, slug: string) => {
    const key = (e.target as HTMLInputElement).id;
    const value = (e.target as HTMLInputElement).value;

    await axios.patch(
        urlJoin(
            getConfig().backend_uri,
            `/guilds/${slug}/update`,
            "?token=" + localStorage.getItem("token")
        ),
        {
            [key]: value,
        }
    );
};

const makeObject = async (k: string | Array<string>, v: string): Promise<Object> => {
    if (typeof(k) == "string") {
        k = k.split(".")
    }

    return {[k[0]]: (k.length == 1) ? v : await makeObject(k.slice(1, k.length), v)};
}

export const saveObjectChanges = async (e: Event, slug: string) => {
    const key = (e.target as HTMLInputElement).id;
    const value = (e.target as HTMLInputElement).value;

    const query = await makeObject(key, value);

    await axios.patch(
        urlJoin(
            getConfig().backend_uri,
            `/guilds/${slug}/update_objects`,
            "?token=" + localStorage.getItem("token")
        ),
        query
    );
};
