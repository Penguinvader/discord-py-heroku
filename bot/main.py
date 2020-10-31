import os
import random
import time
import discord
import asyncio
import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')
lastdel = {}
TOKEN = os.getenv("DISCORD_TOKEN")

structs = os.getenv("STRUCTS")

structlist = [s.strip() for s in structs.split("\n")]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    print("list of visible members:")
    for member in bot.get_all_members():
        print(member)

@bot.event
async def on_message_delete(message):
    lastdel[message.channel] = message

@bot.command()
async def replay(ctx):
    deleted = lastdel[ctx.channel]
    out = discord.Embed(timestamp = deleted.created_at, description = lastdel[ctx.channel].content)
    out.set_author(icon_url = deleted.author.avatar_url, name=deleted.author.name)
    await ctx.send(embed = out)

@bot.command(help="Gives a specified number of random structure decks.")
async def deck(ctx, count=None):
    try:
        out = discord.Embed()
        if count is None or count == "1":
            out.add_field(name = f"{ctx.message.author.name}'s deck:", value = f"{random.choice(structlist)}", inline= True)
            await ctx.send(embed = out)
        elif int(count) < 15:
            decks = random.sample(structlist, k=int(count))
            out.add_field(name = f"{ctx.message.author.name}'s decks:", value = f"{(', '+chr(10)).join(decks)}")
            await ctx.send(embed = out)
        else:
            raise ValueError
    except ValueError:
        await ctx.send(f"The argument has to be an integer with max value 14{'.' if random.randrange(10) < 9 else ', idiot.'}")


@bot.command()
async def roll(ctx):
    await ctx.send(f"{ctx.message.author.mention} rolled {random.randrange(1,101)}!")

@bot.command()
async def coin(ctx):
    await ctx.send(f"{ctx.message.author.mention} flipped {'heads' if random.randrange(2) else 'tails'}!")

@bot.command()
async def bestdeck(ctx):
    msg = await ctx.send(f"Calculating best deck: 0%")
    for i in range(1,5):
        await asyncio.sleep(3)
        await msg.edit(content = f"Calculating best deck: {25*i}%")
    await ctx.send("Calculations complete.\nBest deck: Pendulum")

@bot.command()
async def order(ctx, *args):
    out = ""
    if args:
        arglist = list(args)
        random.shuffle(arglist)
        for place, name in enumerate(arglist,1):
            out += f"{place}. {name}\n"
        await ctx.send(out)
    else:
        await ctx.send("You need to provide at least 1 argument.")

@bot.command()
async def help(ctx):
    out = discord.Embed(title = "Commands:")
    out.add_field(name = "!deck [count]", value = "Generates a random structure deck, count times.", inline= False)
    out.add_field(name = "!roll", value = "Rolls a random number between 1 and 100.", inline= False)
    out.add_field(name = "!coin", value = "Flips a coin.", inline= False)
    out.add_field(name = "!bestdeck", value = "Uses a cutting edge AI model to calculate the best possible Yu-Gi-Oh! deck, based on the current TCG Advanced format.", inline= False)
    out.add_field(name = "!order arg1 arg2 ...", value = "Puts the given arguments in a random order.", inline= False)
    out.add_field(name = "!replay", value = "Replays the last deleted message.", inline= False)
    await ctx.send(embed = out)

if __name__ == "__main__":
    bot.run(TOKEN)
