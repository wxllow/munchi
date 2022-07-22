import glob
import logging
import os

import discord
from discord.ext import commands
from rich.logging import RichHandler

from .config import Config

logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("munchi")

config = Config()

activity = discord.Activity(type=discord.ActivityType.listening, name="commands!")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    application_id=config.application_id,
    activity=activity,
    intents=intents,
    debug_guilds=config.guilds,
)


@bot.event
async def on_ready():
    log.info(f"[bold bright_magenta]:: Bot started!", extra={"markup": True})


def run():
    bot.run(config.token)


def main():
    # Load cogs
    errors = []

    # Get cogs
    initial_cogs = []

    # Get list of cogs from /cogs directory and add them to cogs
    for cog in glob.glob("cogs/**/*.py", recursive=True):
        cog = os.path.normpath(cog).split(os.sep)

        # Remove .py from filename
        if cog[-1].endswith(".py"):
            cog[-1] = cog[-1][:-3]

        initial_cogs.append(".".join(cog))

    initial_cogs += config.cogs

    # Cogs to exclude
    for cog in ["cogs.dev.template"] + config.excluded_cogs:
        initial_cogs.remove(cog)

    for extension in initial_cogs:
        log.info(f"[bright_magenta]:: Loading {extension}", extra={"markup": True})

        try:
            bot.load_extension(extension)
            log.info(f"[bright_green]{extension} loaded!", extra={"markup": True})
        except Exception as e:
            log.exception(e)
            errors.append(extension)
            log.error(f"An error occured while loading {extension}")

    if errors:
        log.warning(
            f"[bright_red]{len(errors)} cogs could not be loaded: {', '.join(errors)}",
            extra={"markup": True},
        )

    run()


if __name__ == "__main__":
    main()
