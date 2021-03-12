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
lastedit = {}
TOKEN = os.getenv("DISCORD_TOKEN")
DECKS = ['deck 1', 'deck 2', 'deck 3', 'deck 4']
decks = []

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
    print(f"Message {message.content} deleted by {message.author}.")
    if message.channel not in lastdel:
        lastdel[message.channel] = [message]
    else:
        lastdel[message.channel].append(message)
        if len(lastdel[message.channel]) > 10:
            lastdel[message.channel].pop(0)

@bot.event
async def on_message_edit(before, after):
    if not after.embeds:
        print(f"Message {before.content} edited to {after.content} by {after.author}.")
        if before.channel not in lastedit:
            lastedit[before.channel] = [before]
        else:
            lastedit[before.channel].append(before)
            if len(lastedit[before.channel]) > 10:
                lastedit[before.channel].pop(0)

@bot.command()
async def replay(ctx, look_back_arg=1):
    look_back = int(look_back_arg)
    if look_back > 10:
        await ctx.send('Max look back value is 10.')
    else:
        deleted = lastdel[ctx.channel][-look_back]
        out = discord.Embed(timestamp=deleted.created_at,
                            description=deleted.content)
        out.set_author(icon_url=deleted.author.avatar_url,
                       name=deleted.author.name)
        await ctx.send(embed=out)


@bot.command()
async def unedit(ctx, look_back_arg=1):
    look_back = int(look_back_arg)
    if look_back > 10:
        await ctx.send('Max look back value is 10.')
    else:
        edited = lastedit[ctx.channel][-look_back]
        out = discord.Embed(timestamp=edited.created_at,
                            description=edited.content)
        out.set_author(icon_url=edited.author.avatar_url,
                       name=edited.author.name)
        await ctx.send(embed=out)

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
async def distribute_deck(ctx, count, *args):
    try:
        out = discord.Embed()
        count = int(count)
        decks = random.sample(structlist, k=count*len(args))
        for i, player in enumerate(args):
            out.add_field(name = f"{player}'s decks:", value = f"{(', '+chr(10)).join(decks[i*count:(i+1)*count])}")
        await ctx.send(embed = out)
    except:
        await ctx.send("Invalid argument(s).")


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
async def yepdeck(ctx, start, stop):
    if ctx.message.author.guild_permissions.ban_members:
        start, stop = int(start), int(stop)
        global decks
        decklist = []
        yeprng = random.Random(777)
        for i in range(1, stop+1):
            if not decks:
                print('currently no decks queued')
                decks = DECKS[::]
                yeprng.shuffle(decks)
                print('random order made:', decks)
            print('sending', decks[0])
            if i >= start:
                decklist.append(decks.pop(0))
            else:
                decks.pop(0)
        out = 'Decks in order:'
        for i, deck in enumerate(decklist, 1):
            out += '\n' + str(i) + '. ' + str(DECKS.index(deck))
        await ctx.send(out)

@bot.command()
async def yepreveal(ctx, deck_no):
    guy = ctx.message.author
    deck_no = int(deck_no)
    if not guy.dm_channel:
        await guy.create_dm()
    await guy.dm_channel.send(DECKS[deck_no])

@bot.command()
async def help(ctx):
    out = discord.Embed(title = "Commands:")
    out.add_field(name = "!deck [count]", value = "Generates a random structure deck, count times, with no repeats.", inline= False)
    out.add_field(name = "!distribute_deck count arg1 arg2 ...", value = "Generates a random structure deck for each extra argument, count times per argument, with no repeats.", inline= False)
    out.add_field(name = "!roll", value = "Rolls a random number between 1 and 100.", inline= False)
    out.add_field(name = "!coin", value = "Flips a coin.", inline= False)
    out.add_field(name = "!bestdeck", value = "Uses a cutting edge AI model to calculate the best possible Yu-Gi-Oh! deck, based on the current TCG Advanced format.", inline= False)
    out.add_field(name = "!order arg1 arg2 ...", value = "Puts the given arguments in a random order.", inline= False)
    out.add_field(name = "!replay [look_back]", value = "Replays the last deleted message.", inline= False)
    out.add_field(name = "!unedit [look_back]", value = "Displays the unedited version of the last edited message.", inline= False)
    await ctx.send(embed = out)

if __name__ == "__main__":
    bot.run(TOKEN)
