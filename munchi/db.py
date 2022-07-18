import enum

from motor.motor_asyncio import AsyncIOMotorClient

from .config import Config

config = Config()


class VCTypes(str, enum.Enum):
    CREATOR = "CREATOR"
    TEMP = "TEMP"


class Database:
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(
            config.db_url,
        )

        self._db = self.client["munchi"]

    @property
    def db(self):
        return self._db
