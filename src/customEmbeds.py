import discord

def play_imbed(title, url, music_queue, converted_time, thumbnail, display_name):
    embed=discord.Embed(title="Rapid Music Player",description=f"[{title}]({url})",color=discord.Color.lighter_grey())
    embed.add_field(name="Queue Position", value=f"Queue: {len(music_queue)}", inline=True)
    embed.add_field(name="Song Duration", value=f"Duration: {converted_time}", inline=True)
    embed.set_thumbnail(url=f"{thumbnail}")
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def play_error_embed(display_name):
    embed=discord.Embed(title="Rapid Music Player",description="Could not download the song. Incorrect format try another keyword. This could be due to a playlist or a livestream format.",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def play_imbed2(title, url, bot_user, thumbnail):
    embed=discord.Embed(title="Rapid Music Player",description=f"[{title}]({url})",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by {bot_user}")
    embed.set_thumbnail(url=f"{thumbnail}")
    return embed

def noconnect_embed(display_name):
    embed=discord.Embed(title="Rapid Music Player",description="You must be connected to a voice channel to use the music bot",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def queue_data(queue_data, display_name):
    embed=discord.Embed(title="Rapid Music Player",description=f"{queue_data}",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def queue_no_music(display_name):
    embed=discord.Embed(title="Rapid Music Player",description="No Music in Queue",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def history_embed(h_data, display_name):
    embed=discord.Embed(title="Rapid Music History",description=f"{h_data}",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def history_clear_embed(display_name):
    embed=discord.Embed(title="Rapid Music History",description="Cleared",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def heads_embed(display_name):
    embed=discord.Embed(title="Rapid Coinflip",description="Heads",color=discord.Color.lighter_grey())
    embed.set_image(url="attachment://heads.png")
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def tails_embed(display_name):
    embed=discord.Embed(title="Rapid Coinflip",description="Tails",color=discord.Color.lighter_grey())
    embed.set_image(url="attachment://tails.png")
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def roll_embed(data, display_name, type, args, sum):
    embed=discord.Embed(title="Rapid Roller",description=f"d{type} {args} Times\n\n{data}\nAmount: {sum}",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def playlist_show_embed(display_name, data):
    embed=discord.Embed(title="Rapid Playlist", description=f"{data}",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def playlist_show_music_embed(display_name, data):
    embed=discord.Embed(title="Rapid Playlist",description=f"{data}",color=discord.Color.lighter_grey())
    embed.set_footer(text=f"Requested by: {display_name}")
    return embed

def help_embed(display_name, client_display_name, client_display_avatar):
    
    information = "Rapid is a bot. A bot that can search for images and music on the interwebs. Here is a list of the commands :smile:"
    music_help = "**-play**, **-stop**, **-resume**, **-pause**, **-queue**, **-skip**"
    playlist_help = "**-playlist create**, **-playlist remove**, **-playlist show**"
    status_help = "**-status game**, **-status stream**, **-status watching**, **-status listening**"
    photos_help = "**-search**, **-get**"
    history_help = "**-history**, **-history clear**"
    tools_help = "**-roll**, **-coinflip**"

    embed=discord.Embed(description=information,color=discord.Color.lighter_grey())
    embed.set_author(name=client_display_name, icon_url=client_display_avatar)
    embed.set_footer(text=f"Requested by: {display_name}")
    embed.add_field(name="🎹 Music",value=music_help, inline=False)
    embed.add_field(name="📖 Music History", value=history_help, inline=False)
    embed.add_field(name="💿 Playlist", value=playlist_help, inline=False)
    embed.add_field(name="🖼️ Images", value=photos_help, inline=False)
    embed.add_field(name="🔧 Tools",value=tools_help,inline=False)
    embed.add_field(name="🇸 Status", value=status_help, inline=False)
    return embed