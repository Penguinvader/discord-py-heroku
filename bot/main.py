import os
import random
import time
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')
TOKEN = os.getenv("DISCORD_TOKEN")
import random

structs = """
[Dragon's Roa](https://www.duelingbook.com/deck?id=2596279)
[Zombie Madness](https://www.duelingbook.com/deck?id=2596284)
[Blaze of Destruction](https://www.duelingbook.com/deck?id=2596277)
[Fury from the Deep](https://www.duelingbook.com/deck?id=2596287)
[Warrior's Triumph](https://www.duelingbook.com/deck?id=2596288)
[Spellcaster's Judgment](https://www.duelingbook.com/deck?id=2596292)
[Invincible Fortress](https://www.duelingbook.com/deck?id=2584605)
[Lord of the Storm](https://www.duelingbook.com/deck?id=2596309)
[Dinosaur's Rage](https://www.duelingbook.com/deck?id=2592591)
[Machine Re-Volt](https://www.duelingbook.com/deck?id=2596312)
[Rise of the Dragon Lords](https://www.duelingbook.com/deck?id=2596326)
[The Dark Emperor](https://www.duelingbook.com/deck?id=2596341)
[Zombie World](https://www.duelingbook.com/deck?id=2596349)
[Spellcaster's Command](https://www.duelingbook.com/deck?id=2596353)
[Warriors' Strike](https://www.duelingbook.com/deck?id=2596356)
[Machina Mayhem](https://www.duelingbook.com/deck?id=2596357)
[Marik](https://www.duelingbook.com/deck?id=2596359)
[Dragunity Legion](https://www.duelingbook.com/deck?id=2595596)
[Lost Sanctuary](https://www.duelingbook.com/deck?id=2596363)
[Gates of the Underworld](https://www.duelingbook.com/deck?id=2595210)
[Dragons Collide](https://www.duelingbook.com/deck?id=2596367)
[Samurai Warlords](https://www.duelingbook.com/deck?id=2596370)
[Realm of the Sea Emperor](https://www.duelingbook.com/deck?id=2596373)
[Onslaught of the Fire Kings](https://www.duelingbook.com/deck?id=2594928)
[Saga of Blue-Eyes White Dragon](https://www.duelingbook.com/deck?id=2596376)
[Cyber Dragon Revolution](https://www.duelingbook.com/deck?id=2594924)
[Realm of Light](https://www.duelingbook.com/deck?id=2596381)
[Geargia Rampage](https://www.duelingbook.com/deck?id=2596388)
[HERO Strike](https://www.duelingbook.com/deck?id=2592906)
[Synchron Extreme](https://www.duelingbook.com/deck?id=2596391)
[Master of Pendulum](https://www.duelingbook.com/deck?id=2594862)
[Emperor of Darkness](https://www.duelingbook.com/deck?id=2596395)
[Rise of the True Dragons](https://www.duelingbook.com/deck?id=2596399)
[Yugi Muto](https://www.duelingbook.com/deck?id=2596403)
[Seto Kaiba](https://www.duelingbook.com/deck?id=2594940)
[Pendulum Domination](https://www.duelingbook.com/deck?id=2594929)
[Machine Reactor](https://www.duelingbook.com/deck?id=2596409)
[Dinosmasher's Fury](https://www.duelingbook.com/deck?id=2594926)
[Cyberse Link](https://www.duelingbook.com/deck?id=2594927)
[Wave of Light](https://www.duelingbook.com/deck?id=2594937)
[Lair of Darkness](https://www.duelingbook.com/deck?id=2596418)
[Powercode Link](https://www.duelingbook.com/deck?id=2594931)
[Zombie Horde](https://www.duelingbook.com/deck?id=3128211)
[Soulburner](https://www.duelingbook.com/deck?id=3073187)
[Order of the Spellcasters](https://www.duelingbook.com/deck?id=3750952)
[Rokket Revolt](https://www.duelingbook.com/deck?id=3959291)
[Shaddoll Showdown](https://www.duelingbook.com/deck?id=4776087)
[Machinized Madness](https://www.duelingbook.com/deck?id=5407162)
[Sacred Beasts](https://www.duelingbook.com/deck?id=5961910)
""".strip()

structlist = [s.strip() for s in structs.split("\n")]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    print("list of visible members:")
    for member in bot.get_all_members():
        print(member)

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
        await ctx.send(f"The argument has to be an integer with max size 14{'.' if random.randrange(10) < 9 else ', idiot.'}")


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
        time.sleep(3)
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
    await ctx.send(embed = out)

if __name__ == "__main__":
    bot.run(TOKEN)
