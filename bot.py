import deck
import discord
from discord.ext import commands
import random

card_deck = deck.Deck()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def getState(ctx):
    await ctx.send(f"`{card_deck.get_state_json()}`")

@bot.command()
async def setState(ctx, *, state):
    check = random.randint(0, 10000)

    await ctx.send(f"Confirm by typing {check}")

    msg = await bot.wait_for('message', check=lambda msg: msg.author == ctx.message.author and msg.channel == ctx.message.channel, timeout=30)

    if msg.content != str(check):
        return

    state = state.replace("`","")
    card_deck.set_state_json(state)
    await ctx.send(f"Restored state to `{card_deck.get_state_json()}`")

@bot.command()
async def drawForTeam(ctx):
    red_role = discord.utils.find(lambda r: r.name == 'Red Team', ctx.message.guild.roles)
    blue_role = discord.utils.find(lambda r: r.name == 'Blue Team', ctx.message.guild.roles)
    is_red = red_role in ctx.message.author.roles
    is_blue = blue_role in ctx.message.author.roles

    if is_red and is_blue:
        await ctx.send("Double agents can't draw!")
        return

    dm_channel = await ctx.message.author.create_dm()

    team = "Red Team" if is_red else "Blue Team"

    check = random.randint(0, 10000)

    await ctx.send(f"Confirm drawing for {team} by typing {check}")

    msg = await bot.wait_for('message', check=lambda msg: msg.author == ctx.message.author and msg.channel == ctx.message.channel, timeout=30)

    if msg.content != str(check):
        return
    
    try:
        card = card_deck.draw(team)
    except:
        await ctx.send("Error: exception when drawing")
        return
    
    await dm_channel.send(f'{team} drew **{card}**')
    
    await ctx.send(f'{team} drew a card!')
    await ctx.send(f'`{card_deck.get_state_json()}`')

@bot.command()
async def drawPublic(ctx):
    red_role = discord.utils.find(lambda r: r.name == 'Red Team', ctx.message.guild.roles)
    blue_role = discord.utils.find(lambda r: r.name == 'Blue Team', ctx.message.guild.roles)
    is_red = red_role in ctx.message.author.roles
    is_blue = blue_role in ctx.message.author.roles

    if is_red and is_blue:
        await ctx.send("Double agents can't draw!")
        return

    check = random.randint(0, 10000)

    await ctx.send(f"Confirm drawing publicly by typing {check}")

    msg = await bot.wait_for('message', check=lambda msg: msg.author == ctx.message.author and msg.channel == ctx.message.channel, timeout=30)

    if msg.content != str(check):
        return
    
    try:
        card = card_deck.draw("Public")
    except:
        await ctx.send("Error: exception when drawing")
        return
    
    await ctx.send(f'Public drew {card}')
    await ctx.send(f'`{card_deck.get_state_json()}`')

@bot.command()
async def hand(ctx):
    red_role = discord.utils.find(lambda r: r.name == 'Red Team', ctx.message.guild.roles)
    blue_role = discord.utils.find(lambda r: r.name == 'Blue Team', ctx.message.guild.roles)
    is_red = red_role in ctx.message.author.roles
    is_blue = blue_role in ctx.message.author.roles

    if is_red and is_blue:
        await ctx.send("Double agents can't look at hands!")
        return
    
    dm_channel = await ctx.message.author.create_dm()

    team = "Red Team" if is_red else "Blue Team"
    
    hand = card_deck.hand(team)

    await dm_channel.send(f"{team}'s hand is: **{', '.join(hand)}**")

@bot.command()
async def handPublic(ctx):
    red_role = discord.utils.find(lambda r: r.name == 'Red Team', ctx.message.guild.roles)
    blue_role = discord.utils.find(lambda r: r.name == 'Blue Team', ctx.message.guild.roles)
    is_red = red_role in ctx.message.author.roles
    is_blue = blue_role in ctx.message.author.roles

    if is_red and is_blue:
        await ctx.send("Double agents can't look at hands!")
        return
    
    hand = card_deck.hand("Public")

    await ctx.send(f"Public hand is: **{', '.join(hand)}**")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    
    channel = bot.get_channel(1551327916887900191)
    
    if channel:
        await channel.send("Deck bot just started!")

card_deck.reset(draw=False) # initialize deck

with open("token.txt", "r") as f:
    bot.run(f.read())