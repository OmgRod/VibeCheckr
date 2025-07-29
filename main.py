import discord
from discord import app_commands
import asyncio
from dotenv import load_dotenv
import os
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch.nn.functional import softmax

load_dotenv()

SETTINGS_FILE = "reaction_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")

emotion_to_emojis = {
    "joy": ["🙂", "😄", "😁"],
    "sadness": ["😔", "😢", "😭"],
    "anger": ["😠", "😡", "🤬"],
    "fear": ["😰", "😨", "😱"],
    "surprise": ["😯", "😲", "😳"],
    "disgust": ["🤨", "🤢", "🤮"],
    "neutral": ["😐", "😑", "😶"]
}

def get_emotion_and_score(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])
    probs = softmax(outputs.logits, dim=1)[0]
    predicted_idx = probs.argmax().item()
    label = model.config.id2label[predicted_idx]
    score = probs[predicted_idx].item()
    return label, score

def choose_emoji(emotion, score):
    if score < 0.6:
        idx = 0
    elif score < 0.85:
        idx = 1
    else:
        idx = 2
    return emotion_to_emojis.get(emotion, ["❓"])[idx]

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.user_reaction_settings = load_settings()

    async def setup_hook(self):
        self.tree.add_command(toggle_reactions)
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/togglereactions"))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not client.user_reaction_settings.get(str(message.author.id), False):
        return

    emotion, score = get_emotion_and_score(message.content.lower())
    emoji = choose_emoji(emotion, score)

    try:
        await message.add_reaction(emoji)
    except discord.HTTPException:
        pass

@app_commands.command(name="togglereactions", description="Toggle automatic emotion reactions on or off for yourself")
async def toggle_reactions(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    current = client.user_reaction_settings.get(user_id, False)
    client.user_reaction_settings[user_id] = not current
    save_settings(client.user_reaction_settings)
    status = "enabled" if not current else "disabled"
    await interaction.response.send_message(f"Your emotion reactions are now {status}.", ephemeral=True)

client.run(os.getenv("BOT_TOKEN"))
