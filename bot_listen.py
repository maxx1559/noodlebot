import discord
import os
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True  # Needed to track speaking and channel joins
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with the user ID you want to monitor
TARGET_USER_ID = 270962054477774848
# Path to your sound file
SOUND_FILE = "fart-with-reverb.mp3"
SONGS = os.listdir("songs")
for song in SONGS:
    print(song)

@bot.command()
async def listen(ctx):
    """Bot joins your current voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Hva' så {channel.name}")
    else:
        await ctx.send("Eyo, du skal være i en voice kanal.")

@bot.command()
async def stopsong(ctx):
    """Bot stops the current song."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Fint, så stopper jeg.")
    else:
        await ctx.send("Eyo, der er ikke noget musik der spiller lige nu.")


@bot.command()
async def stop(ctx):
    """Bot leaves the voice channel it's in."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Fint så smutter jeg også bare.")
    else:
        await ctx.send("Jeg er ikke i nogen voice kanal.")

@bot.command()
async def ralle(ctx,arg=None):
    """Bot plays ralle music"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel

        # Check if bot is already connected to a voice channel
        if ctx.voice_client is not None:
            if ctx.voice_client.channel != channel:
                await ctx.voice_client.move_to(channel)
                await ctx.send(f"Flytter til {channel.name}")
        else:
            await channel.connect()
            await ctx.send(f"Hva' så {channel.name}")

        # Play random song from the list if not already playing
        
        if not ctx.voice_client.is_playing():
            if arg == None:
                song = random.choice(SONGS)
                ctx.voice_client.play(discord.FFmpegPCMAudio("songs/"+song))
                await ctx.send("Spiller lidt lækker musik, vi starter med: " + song.split(".")[0])
                print(f"Playing {song} for {ctx.author.display_name}")
            else:
                # Check if the song is in the list
                song_found = False
                for song in SONGS:
                    if arg.lower() in song.lower():
                        song_found = True
                        ctx.voice_client.play(discord.FFmpegPCMAudio("songs/"+song))
                        await ctx.send("Ok mand, så spiller jeg: " + song.split(".")[0])
                        print(f"Playing {song} for {ctx.author.display_name}")
                        break

                if not song_found:    
                    await ctx.send("Den sang kender jeg sgu ikke.")
                    print(f"Song not found: {arg}")

        else:
            await ctx.send("Gider sgu ikke spille noget - er allerede i gang.")
        
    else:
        await ctx.send("Du skal være i en voice kanal først.")

@bot.command()
async def tracks(ctx):
    """List all available tracks."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await ctx.send("Her er de sange jeg kender:")
        for song in SONGS:
            await ctx.send(song.split(".")[0])
    else:
        await ctx.send("Du skal være i en voice kanal først.")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id != TARGET_USER_ID:
        return

    if before.channel is None and after.channel is not None:
        print(f"🎧 {member.display_name} joined {after.channel.name}")
        vc = member.guild.voice_client
        if vc and vc.channel == after.channel:
            if not vc.is_playing():
                # Play the sound
                vc.play(discord.FFmpegPCMAudio("huntsman-r.e.p.o-sound-made-with-Voicemod.mp3"))
                print(f"🔊 Played sound for {member.display_name}")
            else:
                print(f"⚠️ Already playing audio, skipped sound for {member.display_name}")

    elif before.channel is not None and after.channel is None:
        print(f"👋 {member.display_name} left {before.channel.name}")

    elif before.self_mute != after.self_mute:
        print(f"🔇 {member.display_name} {'muted' if after.self_mute else 'unmuted'} themselves")
        vc = member.guild.voice_client
        if vc and vc.channel == after.channel:
            if not vc.is_playing():
                # Play the sound
                vc.play(discord.FFmpegPCMAudio(SOUND_FILE))
                print(f"🔊 Played sound for {member.display_name}")
            else:
                print(f"⚠️ Already playing audio, skipped sound for {member.display_name}")

    elif before.self_deaf != after.self_deaf:
        print(f"🙉 {member.display_name} {'deafened' if after.self_deaf else 'undeafened'} themselves")

    # Note: You can't detect actual "is speaking" events without audio packets, this is the closest legit thing


bot.run("secret")
