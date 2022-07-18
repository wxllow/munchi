import os
import shutil

import toml


class Config:
    def __init__(self):
        if not os.path.exists("config.toml"):
            shutil.copyfile("resources/config.toml", "config.toml")
            raise Exception(
                "A config file has been created at config.toml. Please edit it and then restart the bot."
            )

        self._config = toml.load("config.toml")

    @property
    def application_id(self):
        return self._config.get("application_id", None)

    @property
    def client_secret(self):
        return self._config.get("client_secret", None)

    @property
    def redirect_uri(self):
        return self._config.get("redirect_uri", None)

    @property
    def token(self):
        return self._config.get("token", None)

    @property
    def tenor_key(self):
        return self._config.get("tenor_key", None)

    @property
    def guilds(self):
        return self._config.get("guild_ids", None)

    @property
    def db_url(self):
        return self._config.get("db_url", "mongodb://localhost:27017")

    @property
    def cogs(self):
        return self._config.get("cogs", [])

    @property
    def excluded_cogs(self):
        return self._config.get("excluded_cogs", [])
