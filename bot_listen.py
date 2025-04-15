import discord
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

@bot.command()
async def listen(ctx):
    """Bot joins your current voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel.name}")
    else:
        await ctx.send("You must be in a voice channel first.")


@bot.command()
async def leave(ctx):
    """Bot leaves the voice channel it's in."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")


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
                vc.play(discord.FFmpegPCMAudio("SOUND_FILE"))
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
