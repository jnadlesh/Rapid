from discord.ext.commands import bot
import customEmbeds as ce
import random as rnd
import discord
import tools
import json

from discord.ext import commands
from image_cog import image_cog
from music_cog import music_cog
from asyncio import sleep





twitch_url = "https://www.twitch.tv/noj___"
s_args = "music | -help"

client = commands.Bot(command_prefix="-")
client.remove_command("help")

client.add_cog(image_cog(client))
client.add_cog(music_cog(client))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=f"{s_args}"))
    print(f"{client.user} is online")

@client.command()
async def status(ctx, type=None, *args):
    if type == None:
        await ctx.send("You need to specify a type: game, stream, listening, watching")
    elif not args:
        await ctx.send("You need to set a message")
    else:
        s_args = " ".join(args)
        if type.lower() == "game":
            await client.change_presence(activity=discord.Game(name=f"{s_args}"))
            await ctx.send("Status Changed")
        elif type.lower() == "stream":
            await client.change_presence(activity=discord.Streaming(name=f"{s_args}", url=twitch_url))
            await ctx.send("Status Changed")
        elif type.lower() == "listening":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=f"{s_args}"))
            await ctx.send("Status Changed")
        elif type.lower() == "watching":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{s_args}"))
            await ctx.send("Status Changed")
        else:
            await ctx.send("You need to specify a proper type: game, stream, listening, watching")

@client.command(name="help")
async def h(ctx):
    await ctx.send(embed=ce.help_embed(ctx.author.display_name, client.user.display_name, client.user.avatar_url))

@client.command(name="coinflip")
async def coinflip(ctx):
    digit = rnd.randint(0,1)
    if digit == 0:
        file = discord.File("C:/Users/JNA/Desktop/Rapid/coinflip-images/heads.png", filename="heads.png")
        await ctx.send(file=file,embed=ce.heads_embed(ctx.author.display_name))
    else:
        file = discord.File("C:/Users/JNA/Desktop/Rapid/coinflip-images/tails.png", filename="tails.png")
        await ctx.send(file=file, embed=ce.tails_embed(ctx.author.display_name))

@client.command(name="roll")
async def roll(ctx, type = None, *args):

    arguments = "".join(args)
    digit_storage = []
    d_data = ""
    d_sum = 0

    if type is None:
        if not args:
            await ctx.send(tools.roll(6))
    else:
        if not args:
            await ctx.send(tools.roll(int(type)))
        else:
            if int(arguments) > 10:
                await ctx.send("Error")
                return
            i = 1
            while i <= int(arguments):
                digit = tools.roll(int(type))
                digit_storage.append(digit)
                i += 1
            increment = 1
            for d in digit_storage:
                d_data = d_data + f"{increment}) {d}\n"
                d_sum = d_sum + d
                increment += 1
            await ctx.send(embed=ce.roll_embed(d_data, ctx.author.display_name, type, arguments, d_sum))

token = ""

#with open("token.txt") as file:
#    token = file.read()

client.run(token)