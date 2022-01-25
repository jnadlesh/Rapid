import blacklist_words as blw
import random as rnd
import discord
import shutil
import os

from google_images_download import google_images_download
from discord.ext import commands
from tools import ddir





word = blw.words

class image_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.download_folder = ddir

        self.keywords = " "

        self.response = google_images_download.googleimagesdownload()

        self.arguments = {
            "keywords": self.keywords,
            "limit": 10,
            "size": "medium",
            "no_directory": True
        }

        self.image_name = []
        self.update_images()

    def update_images(self):
        self.image_name = []
        for filename in os.listdir(self.download_folder):
            self.image_name.append(os.path.join(self.download_folder, filename))

    def clear_folder(self):
        for filename in os.listdir(self.download_folder):
            file_path = os.path.join(self.download_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason %s" % (file_path, e))

    @commands.command()
    async def get(self, ctx):
        images_size = len(self.image_name) - 1 
        random_images = rnd.randint(0, images_size)
        img_path = self.image_name[random_images]

        await ctx.send(file=discord.File(img_path))

    @commands.command()
    async def search(self, ctx, *args):
        self.clear_folder()

        search_args = " ".join(args)
        for i in range(len(word)):
            if word[i] in search_args:
                await ctx.send("You can't search that")
                return
        print(search_args)
        self.arguments["keywords"] = search_args
        self.response.download(self.arguments)

        self.update_images()