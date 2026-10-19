import deck
import discord
from discord.ext import commands
import random

REGIONS = ["Del Rey", "Palms", "Downtown", "Pico-Robertson", "Expo Park", "Fairfax"]
CHALLENGES = ["Lemon", "Okaihau Express", "Bird", "Skip Rock"]

decks = {1561264816314908742: ("region", deck.Deck(REGIONS)), 1561264835100942448: ("challenge", deck.Deck(CHALLENGES))}

# card_deck = deck.Deck()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def getState(ctx):
    """
    Gets the state of this deck. Can restore with >setState state
    """
    await ctx.send(f"`{decks[ctx.channel.id][1].get_state_json()}`")

@bot.command()
async def setState(ctx, *, state):
    """
    Sets the state of this deck.

    Pass something from getState to this
    """
    check = random.randint(0, 10000)

    await ctx.send(f"Confirm for {decks[ctx.channel.id][0]} by typing {check}")

    msg = await bot.wait_for('message', check=lambda msg: msg.author == ctx.message.author and msg.channel == ctx.message.channel, timeout=30)

    if msg.content != str(check):
        return

    state = state.replace("`","")
    decks[ctx.channel.id][1].set_state_json(state)
    await ctx.send(f"Restored state to `{decks[ctx.channel.id][1].get_state_json()}`")

@bot.command()
async def privateDraw(ctx):
    """
    Draw a card from this deck for your team.
    """
    if decks[ctx.channel.id][0] == "challenge":
        await ctx.send("Can't private draw from challenge deck!")
        return

    red_role = discord.utils.find(lambda r: r.name == 'Red Team', ctx.message.guild.roles)
    blue_role = discord.utils.find(lambda r: r.name == 'Blue Team', ctx.message.guild.roles)
    is_red = red_role in ctx.message.author.roles
    is_blue = blue_role in ctx.message.author.roles

    if is_red and is_blue:
        await ctx.send("Double agents can't draw!")
        return
    
    if not (is_red or is_blue):
        await ctx.send("Join a team!")
        return

    dm_channel = await ctx.message.author.create_dm()

    team = "Red Team" if is_red else "Blue Team"

    check = random.randint(0, 10000)

    await ctx.send(f"Confirm drawing for {team} in {decks[ctx.channel.id][0]} by typing {check}")

    msg = await bot.wait_for('message', check=lambda msg: msg.author == ctx.message.author and msg.channel == ctx.message.channel, timeout=30)

    if msg.content != str(check):
        return
    
    try:
        card = decks[ctx.channel.id][1].draw(team)
    except:
        await ctx.send("Error: exception when drawing")
        return
    
    await dm_channel.send(f'{team} drew **{card}**')
    
    await ctx.send(f'{team} drew a card!')
    await ctx.send(f'`{decks[ctx.channel.id][1].get_state_json()}`')

@bot.command()
async def draw(ctx):
    """
    Draw a card from this deck for the public.
    """
    red_role = discord.utils.find(lambda r: r.name == 'Red Team', ctx.message.guild.roles)
    blue_role = discord.utils.find(lambda r: r.name == 'Blue Team', ctx.message.guild.roles)
    is_red = red_role in ctx.message.author.roles
    is_blue = blue_role in ctx.message.author.roles

    if is_red and is_blue:
        await ctx.send("Double agents can't draw!")
        return
    
    if not (is_red or is_blue):
        await ctx.send("Join a team!")
        return

    check = random.randint(0, 10000)

    await ctx.send(f"Confirm drawing publicly in {decks[ctx.channel.id][0]} by typing {check}")

    msg = await bot.wait_for('message', check=lambda msg: msg.author == ctx.message.author and msg.channel == ctx.message.channel, timeout=30)

    if msg.content != str(check):
        return
    
    try:
        card = decks[ctx.channel.id][1].draw("Public")
    except:
        await ctx.send("Error: exception when drawing")
        return
    
    await ctx.send(f'Public drew {card}')
    await publicHand(ctx)
    await ctx.send(f'`{decks[ctx.channel.id][1].get_state_json()}`')

@bot.command()
async def privateHand(ctx):
    """
    View your private hand.
    """
    if decks[ctx.channel.id][0] == "challenge":
        await ctx.send("No private hand for challenge deck!")
        return

    red_role = discord.utils.find(lambda r: r.name == 'Red Team', ctx.message.guild.roles)
    blue_role = discord.utils.find(lambda r: r.name == 'Blue Team', ctx.message.guild.roles)
    is_red = red_role in ctx.message.author.roles
    is_blue = blue_role in ctx.message.author.roles

    if is_red and is_blue:
        await ctx.send("Double agents can't look at hands!")
        return
    
    if not (is_red or is_blue):
        await ctx.send("Join a team!")
        return
    
    dm_channel = await ctx.message.author.create_dm()

    team = "Red Team" if is_red else "Blue Team"
    
    hand = decks[ctx.channel.id][1].hand(team)

    await dm_channel.send(f"{team}'s hand for {decks[ctx.channel.id][0]} is: **{', '.join(hand)}**")

@bot.command()
async def publicHand(ctx):
    """
    View the public hand.
    """
    red_role = discord.utils.find(lambda r: r.name == 'Red Team', ctx.message.guild.roles)
    blue_role = discord.utils.find(lambda r: r.name == 'Blue Team', ctx.message.guild.roles)
    is_red = red_role in ctx.message.author.roles
    is_blue = blue_role in ctx.message.author.roles

    if is_red and is_blue:
        await ctx.send("Double agents can't look at hands!")
        return
    
    if not (is_red or is_blue):
        await ctx.send("Join a team!")
        return
    
    hand = decks[ctx.channel.id][1].hand("Public")

    await ctx.send(f"Public hand for {decks[ctx.channel.id][0]} is: **{', '.join(hand)}**")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    
    channel = bot.get_channel(1551327916887900191)
    
    if channel:
        await channel.send("Deck bot just started!")

@bot.event
async def on_message(message):
    if "okaihau" in message.content.lower() and not message.author.bot:
        await message.channel.send("She starts out from Otiria, the smallest train you've seen")
    
    if "She starts out from Otiria, the smallest train you've seen".lower() in message.content.lower():
        await message.channel.send("This is the Okaihau Express")

    await bot.process_commands(message)

for deck in decks.values():
    deck[1].reset(draw=False) # initialize deck

with open("token.txt", "r") as f:
    bot.run(f.read())