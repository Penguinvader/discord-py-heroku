import os
import random
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")
import random

structs = """
    Structure Deck: Blaze of Destruction
    Cyber Dragon Revolution Structure Deck
    Structure Deck: Cyberse Link
    Structure Deck: Dinosaur's Rage
    Dinosmasher's Fury Structure Deck
    Structure Deck: Dragon's Roar
    Dragons Collide Structure Deck
    Dragunity Legion Structure Deck
    Emperor of Darkness Structure Deck
    Structure Deck: Freezing Chains
    Structure Deck: Fury from the Deep
    Gates of the Underworld Structure Deck
    Geargia Rampage Structure Deck
    HERO Strike Structure Deck
    Structure Deck: Invincible Fortress
    Structure Deck: Lord of the Storm
    Lost Sanctuary Structure Deck
    Machina Mayhem Structure Deck
    Structure Deck: Machine Re-Volt
    Machine Reactor Structure Deck
    Structure Deck: Marik (TCG)
    Master of Pendulum Structure Deck
    Structure Deck: Mechanized Madness
    Onslaught of the Fire Kings Structure Deck
    Structure Deck: Order of the Spellcasters
    Pendulum Domination Structure Deck
    Structure Deck: Powercode Link
    Realm of Light Structure Deck
    Realm of the Sea Emperor Structure Deck
    Rise of the Dragon Lords Structure Deck
    Rise of the True Dragons Structure Deck
    Structure Deck: Rokket Revolt
    Structure Deck: Sacred Beasts
    Saga of Blue-Eyes White Dragon Structure Deck
    Samurai Warlords Structure Deck
    Structure Deck: Seto Kaiba
    Structure Deck: Shaddoll Showdown
    Structure Deck: Soulburner
    Spellcaster's Command Structure Deck
    Structure Deck: Spellcaster's Judgment
    Structure Deck: Spirit Charmers
    Structure Deck: Lair of Darkness
    Structure Deck: Wave of Light
    Synchron Extreme Structure Deck
    The Dark Emperor Structure Deck
    Structure Deck: Warrior's Triumph
    Warriors' Strike Structure Deck
    Structure Deck: Yugi Muto
    Structure Deck: Zombie Horde
    Structure Deck: Zombie Madness
    Zombie World Structure Deck
""".strip()

structlist = [s.strip() for s in structs.split("\n")]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def deck(ctx):
    await ctx.send(f"{ctx.message.author.mention}, your deck is: {random.choice(structlist)}")

@bot.command()
async def roll(ctx):
    await ctx.send(f"{ctx.message.author.mention} rolled {random.randrange(1,101)}!")

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

if __name__ == "__main__":
    bot.run(TOKEN)
