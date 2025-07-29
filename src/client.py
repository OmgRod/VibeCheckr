import discord
from discord import app_commands
from src.settings import load_settings, save_settings
from src.emotion import get_emotion_and_score, choose_emoji
from src.commands import toggle_reactions
from src.metrics import register_message

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.user_reaction_settings = load_settings()

    async def setup_hook(self):
        self.tree.add_command(toggle_reactions(self))
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/togglereactions"))

    async def on_message(self, message):
        if message.author.bot:
            return

        if not self.user_reaction_settings.get(str(message.author.id), False):
            return

        emotion, score = get_emotion_and_score(message.content.lower())
        emoji = choose_emoji(emotion, score)
        register_message(emotion)

        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            pass
