import customEmbeds as ce
import datetime
import discord
import shutil
import tools
import json
import os 

from discord.ext import commands
from youtube_dl import YoutubeDL
from tools import hdir, sdir, pdir





playlist = ["juice", "juicer", "hype"]
stop = "🛑"
song_limit = 25

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

        self.music_history_info = {"title": "", "duration": "", "thumbnail": "", "url": ""}

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        self.music_history_info = {"title": info["title"], "duration": info["duration"], "thumbnail": info["thumbnail"], "url": f"https://youtube.com/watch?v={info['id']}"}
        tc = datetime.timedelta(seconds=self.music_history_info['duration'])
        self.converted_time = str(tc)
        tools.save_data(self.music_history_info['title'],self.music_history_info['url'],self.converted_time,self.music_history_info['thumbnail'])

        return {'source': info['formats'][0]['url'], 'title': info['title']} 

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            with open(f"{sdir}.json", "w") as f:
                data = self.music_history_info
                json.dump(data, f, indent=4)
        
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False
    
    @commands.command(name="play")
    async def play(self, ctx, *args):
        query = " ".join(args)
        if ctx.author.voice is None:
            await ctx.send(embed=ce.noconnect_embed(ctx.author.display_name))
        else:
            voice_channel = ctx.author.voice.channel
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send(embed=ce.play_error_embed(ctx.author.display_name))
            else:
                self.music_queue.append([song, voice_channel])
                print(f"\n[playing/enqueued] {self.music_history_info['title']} | {self.music_history_info['url']} | {self.converted_time} to play in {self.music_queue[0][1]}\n")
                await ctx.send(embed=ce.play_imbed(self.music_history_info['title'],self.music_history_info['url'],self.music_queue,self.converted_time,self.music_history_info['thumbnail'],ctx.author.display_name))

                if self.is_playing == False:
                    await self.play_music()


    @commands.command(name="queue")
    async def queue(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=ce.noconnect_embed(ctx.author.display_name))
        else:
            queue_data = ""
            for i in range(len(self.music_queue)):
                queue_data += f"{i + 1}) {self.music_queue[i][0]['title']}\n"
            
            if queue_data != "":
                await ctx.send(embed=ce.queue_data(queue_data, ctx.author.display_name))
            else:
                await ctx.send(embed=ce.queue_no_music(ctx.author.display_name))

    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=ce.noconnect_embed(ctx.author.display_name))
        else:
            if self.vc != "" and self.vc:
                ctx.voice_client.stop()
                if len(self.music_queue) > 0:
                    self.play_next()
                else:
                    await self.play_music()

    @commands.command(name="stop")
    async def stop(self, ctx):

        message_id = ctx.message.id
        msg = await ctx.fetch_message(message_id)

        if ctx.author.voice is None:
            await ctx.send(embed=ce.noconnect_embed(ctx.author.display_name))
        else:
            if ctx.voice_client:
                self.music_queue = []
                await ctx.voice_client.disconnect()
                await msg.add_reaction(stop)

    @commands.command(name="pause")
    async def pause(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=ce.noconnect_embed(ctx.author.display_name))
        else:
            if not ctx.voice_client:
                await ctx.send("I'm not connceted")
                return
            if ctx.voice_client.is_playing() == False:
                await ctx.send("Rapid is not playing any music")
            else:
                await ctx.send("Pausing")
                ctx.voice_client.pause()

    @commands.command(name="resume")
    async def resume(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(embed=ce.noconnect_embed(ctx.author.display_name))
        else:
            if not ctx.voice_client:
                await ctx.send("I'm not connected")
                return
            if self.vc.is_playing():
                await ctx.send("Rapid is already playing")
            else:
                await ctx.send("Resuming")
                ctx.voice_client.resume()

    @commands.command(name="history")
    async def history(self, ctx, *args):
        arguments = " ".join(args)
        if not args:
            files = []
            h_data = ""
            i = 0
            os.chdir(hdir)
            result = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime, reverse=True)
            for a in range(len(result)):
                h_data = "".join([result[a]])
                files.append(h_data)
            if len(files) <= song_limit:
                h_data = ""
                for i in range(len(files)):
                    with open(f"{hdir}/{files[i]}") as f:
                        data = json.load(f)
                        history_data = {"title": data["title"],"url": data["url"],"duration": data["duration"],"thumbnail": data["thumbnail"]}
                        i += 1
                    h_data += f"{i}) [{history_data['title']}]({history_data['url']}) \n"
            elif len(files) > song_limit:
                h_data = ""
                i = 0
                for i in range(song_limit):
                    with open(f"{hdir}/{files[i]}") as f:
                        data = json.load(f)
                        history_data = {"title": data["title"],"url": data["url"],"duration": data["duration"],"thumbnail": data["thumbnail"]}
                        i += 1
                    h_data += f"{i}) [{history_data['title']}]({history_data['url']}) \n"
            await ctx.send(embed=ce.history_embed(h_data, ctx.author.display_name))

        elif arguments.lower() == "clear":
            for filename in os.listdir(hdir):
                file_path = os.path.join(hdir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason %s" % (file_path, e))
            await ctx.send(embed=ce.history_clear_embed(ctx.author.display_name))
        else:
            print("Error")

    @commands.command(name="playlist")
    async def playlist(self, ctx, type=None, *args):
        if type == None:
            await ctx.send("You need to specify a type.")
        else:
            if type == "create":
                arguments = " ".join(args)
                if not args:
                    await ctx.send(f"Must have a name")
                    return
                else:
                    await tools.check_dir(ctx, arguments)

            elif type == "remove":
                arguments = " ".join(args)
                if f"{arguments}.json" not in os.listdir(pdir):
                    await ctx.channel.send(f"{arguments} does not exist.")
                else:
                    os.remove(f"{pdir}/{arguments}.json")
                    await ctx.channel.send(f"Playlist removed: \"{arguments}\"!")

            elif type == "show":
                arguments = " ".join(args)
                if not args:
                    await tools.show_dir(ctx)
                else:
                    await tools.show_dir_info(ctx, arguments)
                
            else:
                await ctx.send("That is not a valid command")

    @commands.command(name="playlistadd")
    async def playlistadd(ctx, *args):
        if not args:
            await ctx.send("Add")

    @commands.command(name="playlistremove")
    async def playlistremove(ctx, *args):
        if not args:
            await ctx.send("Remove")

