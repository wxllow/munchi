import discord
from discord.ext import commands
from humanfriendly import InvalidTimespan

errors = {
    InvalidTimespan: "Invalid timespan.",
    commands.BadArgument: "Invalid argument.",
    commands.BotMissingPermissions: "I don't have permissions to execute this command.",
    commands.BotMissingRole: "I don't have the required role to execute this command.",
    commands.ChannelNotFound: ":question: The channel {err.argument} does not exist.",
    commands.CommandNotFound: ":question: This command does not exist.",
    commands.CommandOnCooldown: ":hourglass_flowing_sand: Please wait another {round(e.retry_after)} seconds before using this command again.",
    commands.EmojiNotFound: ":question: Emoji {err.argument} does not exist.",
    commands.GuildNotFound: ":question: The server {err.argument} does not exist.",
    commands.MaxConcurrencyReached: "This command has reached its maximum uses.",
    commands.MemberNotFound: ":question: The member {err.argument} does not exist.",
    commands.MessageNotFound: ":question: The message {err.argument} does not exist.",
    commands.MissingPermissions: "You don't have permission to use this command.",
    commands.MissingRequiredArgument: "{err.param} is a required argument.",
    commands.MissingRole: "You don't have the required role to use this command.",
    commands.NSFWChannelRequired: ":underage: This command can only be used in NSFW channels :flushed:",
    commands.NoPrivateMessage: "This command can only be used in a server.",
    commands.NotOwner: "Only the bot owner can use this command.",
    commands.PrivateMessageOnly: "This command can only be used in private messages.",
    commands.RoleNotFound: ":question: The role {err.argument} does not exist.",
    commands.UserNotFound: ":question: The member {err.argument} does not exist.",
}


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, exception):
        try:
            msg = errors[type(exception)].format(err=exception)
        except KeyError:
            embed = discord.Embed(
                title=":warning: An unknown error has occurred",
                description=str(exception),
                colour=discord.Colour.red(),
            )
            embed.set_footer(
                text="You can report issues at https://github.com/wxllow/munchi/issues"
            )
            await ctx.respond(embed=embed)

            raise exception

        embed = discord.Embed(
            title=":warning: Error", description=msg, color=discord.Color.red()
        )

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
