import customEmbeds as ce
import random as rnd
import discord
import json
import os





hdir = "C:/Users/JNA/Desktop/Rapid/src/history"
ddir = "C:/Users/JNA/Desktop/Rapid/src/downloads"
sdir = "C:/Users/JNA/Desktop/Rapid/src/stored"
pdir = "C:/Users/JNA/Desktop/Rapid/src/playlists"

def wordScrambler(l):
    word = ""
    for i in range(len(l)):
        if i%2 == 0:
            word += l[i].upper()
        else:
            word += l[i].lower()
    return word

def roll(amount):
    digit = rnd.randint(1,amount)
    return digit

def save_data(title, url, duration, thumbnail):
    history_data = {"title": title, "url": url, "duration": duration, "thumbnail": thumbnail}
    files = []
    if not os.listdir(hdir):
        with open(f"{hdir}/song{1}.json", "w") as f:
            data = history_data
            json.dump(data, f, indent=4)
    else:
        for filename in os.listdir(f"{hdir}"):
            files.append(filename)
        with open(f"{hdir}/song{len(files) + 1}.json", "w") as f:
            data = history_data
            json.dump(data, f, indent=4)

async def save_query(ctx, args):
    with open(f"{pdir}/{args}.json", "w") as f:
        json.dump(f"New Playlist: {args}", f, indent=4)
    await ctx.send(f"Playlist created: {args}")

async def check_dir(ctx, *args):
    arguments = " ".join(args)
    arguments = arguments
    data = []
    if len(os.listdir(pdir)) == 0:
        print("File does not exist, creating file.")
        await save_query(ctx, arguments)
    else:
        for filename in os.listdir(pdir):
            data.append(filename)
            if arguments + ".json" in data:
                print("File already exists.")
                await ctx.send(f"Playlist,\"{arguments}\" already exists.")
                return
            else:
                print("File does not exist, creating file.")
                await save_query(ctx, arguments)
                return

async def show_dir(ctx): 
    s_data = ""
    if len(os.listdir(pdir)) == 0:
        await ctx.send("There are no playlists.")
    else:
        i = 1
        for filename in os.listdir(pdir):
            s_data += f"{i}) {filename.strip('.json')} \n"
            i += 1
        await ctx.send(embed=ce.playlist_show_embed(ctx.author.display_name, s_data))

async def show_dir_info(ctx, *args):
    arguments = " ".join(args)
    print(arguments)
    s_data = ""
    stored = []
    i = 1
    for filename in os.listdir(pdir):
        stored.append(filename)
    if f"{arguments}.json" not in stored:
        await ctx.send("Error: N/A")
    if f"{arguments}.json" in stored:
        with open(f"{pdir}/{arguments}.json", "r") as f:
            data = json.load(f)
            s_data += f"{data}\n"
            i += 1
        await ctx.send(embed=ce.playlist_show_music_embed(ctx.author.display_name, s_data))


            


