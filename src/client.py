import discord
import random
from discord import app_commands
from src.settings import load_settings, save_settings
from src.emotion import get_emotion_and_score, choose_emoji
from src.commands import toggle_reactions_command, set_custom_emojis_command, set_reaction_chance_command, reset_emojis_command
from src.metrics import register_message

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.user_reaction_settings = load_settings("user_reaction_settings")

    async def setup_hook(self):
        self.tree.add_command(toggle_reactions_command(self))
        self.tree.add_command(set_reaction_chance_command(self))
        self.tree.add_command(set_custom_emojis_command(self))
        self.tree.add_command(reset_emojis_command(self))
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/togglereactions"))

    async def on_message(self, message):
        if message.author.bot:
            return

        settings = self.user_reaction_settings.get(str(message.author.id), {"enabled": True, "reaction_chance": 100})

        if isinstance(settings, bool):
            enabled = settings
            chance = 100
        else:
            enabled = settings.get("enabled", True)
            chance = settings.get("reaction_chance", 100)

        if not enabled or random.randint(1, 100) > chance:
            return

        emotion, score = get_emotion_and_score(message.content.lower())
        emoji = choose_emoji(emotion, score, message.guild.id if message.guild else None, self)
        register_message(emotion)

        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            pass
