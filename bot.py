import discord
from tavily import TavilyClient
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import re
import os

from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask
from threading import Thread

# =========================
# LOAD ENV FILE
# =========================
load_dotenv()
app = Flask('')

@app.route('/')
def home():
    return "R2-D2 is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# =========================
# BOT TOKEN
# =========================
TOKEN = os.getenv("TOKEN")
client = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=os.getenv("OPENROUTER_API_KEY")

)
tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)
# =========================
# BOT INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# =========================
# CREATE BOT
# =========================
bot = commands.Bot(command_prefix="!", intents=intents)

# REMOVE DEFAULT HELP
bot.remove_command("help")

# =========================
# BLOCKED WORDS
# =========================
blocked_words = [

    # English
    "fuck",
    "fk",
    "fku",
    "shit",
    "bitch",
    "bastard",
    "cunt",
    "piss",
    "asshole",
    "motherfucker",
    "dick",
    "cock",
    "prick",
    "pussy",
    "wanker",
    "bollocks",
    "bloody",
    "twat",
    "bugger",
    "douchebag",
    "ass",
    "bullshit",
    "jackass",
    "horseshit",
    "slut",
    "whore",
    "nigger",
    "nigga",

    # Hindi
    "bhenchod",
    "madarchod",
    "bhadwa",
    "chutiya",
    "harami",
    "kaminey",
    "gaand",
    "lund",
    "tatto",
    "choot",
    "randi",
    "kuttiya",
    "bsdk",
    "mc",
    "bc",
    "randi",
    "gandu",
    "gand",
    "mkc",
    "kutta",
    

    # Kannada / Kanglish
    "bolimaga",
    "sulemaga",
    "husi",
    "shata",
    "lofa",
    "key",
    "thika",
    "hadaragithi",
    "boli",
    "sule",
    "suule",
    "mindri",
    "mindrimaga",
    "mindrimagane",
    "bolimagane",
    "sulemagane",
    "tikamucho"

]

# =========================
# BOT ONLINE EVENT
# =========================
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

# =========================
# MEMBER JOIN EVENT
# =========================
@bot.event
async def on_member_join(member):

    role = discord.utils.get(member.guild.roles, name="Member")

    if role:
        await member.add_roles(role)

    channel = discord.utils.get(member.guild.text_channels, name="general")

    if channel:

        embed = discord.Embed(
            title="🚀 Welcome to The Backend Club",
            description=f"Welcome {member.mention}!",
            color=0x5865F2
        )

        embed.add_field(
            name="Build. Ship. Scale.",
            value="Glad to have you here.",
            inline=False
        )

        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )

        await channel.send(embed=embed)

# =========================
# MESSAGE FILTER
# =========================
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    # ALLOW MEMES CHANNEL
    if message.channel.name == "memes":
        await bot.process_commands(message)
        return

    content = message.content.lower()

    # SPAM FILTER
    if re.search(r"(.)\1{8,}", content):

        await message.delete()

        warn = await message.channel.send(
            f"⚠️ {message.author.mention} Spam detected."
        )

        await warn.delete(delay=5)
        return

    # BAD WORD FILTER
    for word in blocked_words:

        if re.search(rf"\b{re.escape(word)}\b", content):

            await message.delete()

            warn = await message.channel.send(
                f"⚠️ {message.author.mention} Keep the chat clean."
            )

            await warn.delete(delay=5)
            return

    await bot.process_commands(message)

# =========================
# PING COMMAND
# =========================
@bot.command()
async def ping(ctx):

    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: {latency}ms",
        color=0x57F287
    )

    await ctx.send(embed=embed)

# =========================
# ABOUT COMMAND
# =========================
@bot.command()
async def about(ctx):

    embed = discord.Embed(
        title="🚀 The Backend Club",
        description="Build. Ship. Scale.",
        color=0x5865F2
    )

    embed.add_field(
        name="About",
        value="A community of developers, builders and creators.",
        inline=False
    )

    await ctx.send(embed=embed)

# =========================
# HELP COMMAND
# =========================
@bot.command()
async def help(ctx):

    embed = discord.Embed(
        title="📘 Commands",
        description="Available bot commands",
        color=0x5865F2
    )

    embed.add_field(name="!ping", value="Check bot latency", inline=False)
    embed.add_field(name="!about", value="About server", inline=False)
    embed.add_field(name="!server", value="Server information", inline=False)
    embed.add_field(name="!user", value="Your profile info", inline=False)
    embed.add_field(name="!avatar", value="Show avatar", inline=False)
    embed.add_field(name="!clear 5", value="Delete messages", inline=False)

    embed.set_footer(text="The Backend Club")

    await ctx.send(embed=embed)

# =========================
# SERVER INFO
# =========================
@bot.command()
async def server(ctx):

    guild = ctx.guild

    embed = discord.Embed(
        title="🌐 Server Info",
        color=0x5865F2
    )

    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Members", value=guild.member_count, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    await ctx.send(embed=embed)

# =========================
# USER INFO
# =========================
@bot.command()
async def user(ctx):

    member = ctx.author

    embed = discord.Embed(
        title="👤 User Info",
        color=0x5865F2
    )

    embed.add_field(name="Username", value=member.name, inline=False)

    embed.add_field(
        name="Joined Server",
        value=member.joined_at.strftime("%d/%m/%Y"),
        inline=False
    )

    embed.set_thumbnail(
        url=member.avatar.url if member.avatar else member.default_avatar.url
    )

    await ctx.send(embed=embed)

# =========================
# AVATAR COMMAND
# =========================
@bot.command()
async def avatar(ctx):

    member = ctx.author

    embed = discord.Embed(
        title=f"{member.name}'s Avatar",
        color=0x5865F2
    )

    embed.set_image(
        url=member.avatar.url if member.avatar else member.default_avatar.url
    )

    await ctx.send(embed=embed)

# =========================
# CLEAR COMMAND
# =========================
@bot.command()
async def clear(ctx, amount=5):

    await ctx.channel.purge(limit=amount)
# =========================
# AI COMMAND
# =========================
@bot.command()
@cooldown(1, 10, BucketType.user)
async def ai(ctx, *, prompt):

    thinking = await ctx.send("🤖 Thinking...")

    try:

        # SEARCH INTERNET
        search = tavily.search(
            query=prompt,
            max_results=3
        )

        search_context = ""

        for result in search.get("results", []):
            search_context += f"""
Title:
{result['title']}

Content:
{result['content']}

URL:
{result['url']}

"""

        # BUILD MESSAGES
        messages = [
            {
                "role": "system",
                "content": """
You are an elite software engineering assistant inside Discord.

Rules:
- Keep responses concise.
- Prefer code over explanations.
- Use modern libraries/frameworks.
- Avoid deprecated tools.
- Use live search results if relevant.
- Generate clean runnable code.
- Optimize responses for Discord readability.
"""
            },
            {
                "role": "user",
                "content": f"""
User Question:
{prompt}

Live Web Search Results:
{search_context}
"""
            }
        ]

        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=messages,
            temperature=0.5,
            top_p=0.9,
            max_tokens=900
        )

        answer = response.choices[0].message.content

        # EMPTY RESPONSE FIX
        if not answer:
            answer = "⚠️ Model returned empty response."

        # DELETE THINKING MESSAGE
        await thinking.delete()

        # CLEAN RESPONSE
        answer = answer.strip()

        # SMART CHUNKING
        chunks = []

        current_chunk = ""

        lines = answer.split("\n")

        for line in lines:

            # IF CHUNK TOO BIG
            if len(current_chunk) + len(line) + 1 > 1800:

                chunks.append(current_chunk)

                current_chunk = ""

            current_chunk += line + "\n"

        # ADD LAST CHUNK
        if current_chunk:
            chunks.append(current_chunk)

        # SEND CHUNKS
        for chunk in chunks:

            chunk = chunk.strip()

            # DETECT CODE
            if (
                "def " in chunk
                or "class " in chunk
                or "import " in chunk
                or "print(" in chunk
                or "return " in chunk
                or "for " in chunk
                or "while " in chunk
            ):

                formatted = f"```python\n{chunk}\n```"

            else:

                formatted = chunk

            embed = discord.Embed(
                description=formatted,
                color=0x5865F2
            )

            await ctx.send(embed=embed)

    except Exception as e:

        await thinking.edit(
            content=f"❌ Error: {e}"
        )
@ai.error
async def ai_error(ctx, error):

    if isinstance(error, commands.CommandOnCooldown):

        await ctx.send(
            f"⏳ Slow down. Try again in {round(error.retry_after, 1)}s."
        )
# =========================
# START BOT
# =========================
bot.run(TOKEN)