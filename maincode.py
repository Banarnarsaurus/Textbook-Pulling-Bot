import logging

import aiohttp
import discord
from discord.ext import commands

import menus
import paginate
import textbook_puller

no_result_message = """Sorry, we can\'t find this book D:"""
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="$")
bot.client = None
bot.textbook = None


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    bot.client = aiohttp.ClientSession()
    bot.textbook = textbook_puller.FreeLibrary(bot.client)
    await bot.tree.sync(guild=discord.Object(829177539263070218))
    print("synced cmd tree")


@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)


@bot.event
async def on_close():
    await bot.client.close()


@discord.app_commands.guilds(829177539263070218)
@bot.hybrid_command()
async def search(ctx: commands.Context, *, search: str):
    await ctx.defer()

    key_words, search_words = bot.textbook.keywords_search_words(search)
    print('content' + ctx.message.content)
    print('search' + search)
    result_links = await bot.textbook.search(key_words)
    links = bot.textbook.send_link(result_links, search_words)

    if len(links) > 0:
        commands.Paginator()
        textbook_links = [f'https://usa1lib.org{link}' for link in links]
        source = paginate.ContentSource(textbook_links, per_page=1)
        menu = paginate.Pages(
            interaction=ctx.interaction if ctx.interaction else ctx,
            source=source,
            bot=bot,
            compact=True
        )
        await menu.start()

    else:
        await ctx.send(no_result_message)


bot.run(
    "insert token here",
    log_level=logging.WARNING,
)
print("sus much")
