from discord.ext import commands
import discord
from ApiHelpers import daily_stats, monthly_stats, find_total_count, today_stats
from Validators import validate_format_month, validate_format_day
from OtherHelpers import datetime_formatted_in_kyiv, format_monthly_date, format_daily_date

TOKEN = '{YOUR_TOKEN_HERE}'

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix=".u ", intents=discord.Intents.all())

EMBED_COLOUR = discord.Colour.from_rgb(255, 215, 0)
FOOTER = "Note: The provided data is subject to potential inaccuracies and may not be entirely reliable. "

key_mapping = {
    "tanks": "🛡️ Tanks",
    "apv": "🚐 Armoured Personnel Carriers",
    "artillery": "🎯 Artillery",
    "mlrs": "💥 Rocket Artillery",
    "aaws": "🦅 Anti-Aircraft systems",
    "aircraft": "✈️ Aircraft",
    "helicopters": "🚁 Helicopters",
    "uav": "🛩 UAVs",
    "vehicles": "🚗 Vehicles",
    "boats": "⚓️ Boats",
    "submarines": "🤿 Submarines",
    "se": "🚜 Special Equipment",
    "missiles": "🚀 Cruise Missiles",
    "personnel": "💂🏻‍♀️ Personnel",
    "captive": "⛓️ Captive"
}

@bot.command()
async def today(ctx):
    summed, latest = today_stats()

    date = datetime_formatted_in_kyiv()
    embed = discord.Embed(
        colour=EMBED_COLOUR,
        title=f"Russian losses as of today ({date} Kyiv time)",
        description="Hello from Kyiv! As of today, the occupying forces have suffered the following losses:"
    )
    embed.set_footer(text=FOOTER)
    embed.set_thumbnail(url="attachment://RULOSSES.png")

    for key, value in summed.items():
        key_name = key_mapping[key]
        value = f"{value}" + (f" **(+{latest[key]})**" if latest[key] > 0 else "")
        embed.add_field(name=key_name, value=value, inline=False)

    await ctx.send(embed=embed,file=discord.File("./static/RULOSSES.png"))


@bot.command()
async def monthly(ctx, date: str):
    # Validating the date format
    if not validate_format_month(date):
        await ctx.send("Oops! The date format doesn't seem right. Please ensure it follows the format of yyyy.mm (e.g., 2022.02).")
        return

    # Retrieving the data
    data, message = monthly_stats(date)

    # Notifying the user if any errors occurred
    if data is None:
        await ctx.send(message)
        return

    # Creating the embed
    date_formatted = format_monthly_date(date)
    embed = discord.Embed(
        colour=EMBED_COLOUR,
        title=f"Russian losses in {date_formatted}",
    )
    embed.set_footer(text=FOOTER)
    embed.set_thumbnail(url="attachment://RULOSSES.png")

    for key, value in data.items():
        if value > 0:
            key_name = key_mapping[key]
            embed.add_field(name=key_name, value=f"+{value}", inline=False)

    await ctx.send(embed=embed, file=discord.File("./static/RULOSSES.png"))


@bot.command()
async def daily(ctx, date: str):
    # Validating the date format
    if not validate_format_day(date):
        await ctx.send("Oops! The date format doesn't seem right. Please ensure it follows the format of yyyy.mm.dd (e.g., 2022.02.24).")
        return

    # Retrieving the data
    data, message = daily_stats(date)

    # Notifying the user if any errors occurred
    if data is None:
        await ctx.send(message)
        return

    # Creating the embed
    date_formatted = format_daily_date(date)
    embed = discord.Embed(
        colour=EMBED_COLOUR,
        title=f"Russian losses on {date_formatted}",
    )
    embed.set_footer(text=FOOTER)
    embed.set_image(url="attachment://RULOSSES.png")

    for key, value in data.items():
        if value > 0:
            key_name = key_mapping[key]
            embed.add_field(name=key_name, value=f"+{value}", inline=False)

    await ctx.send(embed=embed, file=discord.File("./static/RULOSSES.png"))


@bot.command()
async def sos(ctx):
    embed = discord.Embed(
        colour=EMBED_COLOUR,
        title="Need help?",
        description="Let me provide you with a brief set of instructions of how I can be handy."
    )
    embed.add_field(name='🔷 To call a command use the following prefix ".u" and the command name afterwards, both seperated by a space character.', value='\u200b', inline=False)
    embed.add_field(name='🔷 I currently support the given commands:', value='🔸 **today** - provides you with latest data'
                                                                         '\n'
                                                                         '🔸 **daily {date}** - provides you with daily data of a specific date, provided by the user in the format of yyyy.mm.dd '
                                                                         '\n'
                                                                         '🔸 **monthly {date}** - provides you with monthly data of a specific date, provided by the user in the format of yyyy.mm'
                    ,inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_guild_join(server):
    announce_channel = None
    for channel in server.text_channels:
        if 'general' in channel.name:
            announce_channel = channel
            break
    if announce_channel is None:
        announce_channel = server.text_channels[0]

    if announce_channel and announce_channel.permissions_for(server.me).send_messages:
        await announce_channel.send('Hi there! I help you keep up with the losses of Russian Armed Forces within the Russo-Ukrainian war. Use the command ".u sos" to get familiar with my functionality.')



bot.run(TOKEN)