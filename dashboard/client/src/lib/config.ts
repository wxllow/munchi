export function getConfig() {
    return {
        "backend_uri": import.meta.env.DEV ? "http://127.0.0.1:8080/" : "https://backend.munchi.wxllow.dev/",
        "client_uri": import.meta.env.DEV ? "http://127.0.0.1:3000/" : "https://munchi.wxllow.dev/",
        "application_id": import.meta.env.DEV ? "992952954598457476" : "967137754024669284"
    }
}
