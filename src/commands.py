from discord import app_commands, Interaction
from discord.app_commands import Choice
from src.settings import save_settings, load_settings

emotion_choices = [
    Choice(name="joy", value="joy"),
    Choice(name="sadness", value="sadness"),
    Choice(name="anger", value="anger"),
    Choice(name="fear", value="fear"),
    Choice(name="surprise", value="surprise"),
    Choice(name="disgust", value="disgust"),
    Choice(name="neutral", value="neutral"),
]

def toggle_reactions_command(client):
    @app_commands.command(name="togglereactions", description="Toggle automatic emotion reactions on or off for yourself")
    async def _toggle(interaction: Interaction):
        try:
            user_id = str(interaction.user.id)
            current = client.user_reaction_settings.get(user_id, {"enabled": False, "reaction_chance": 100})
            if isinstance(current, bool):
                current = {"enabled": not current, "reaction_chance": 100}
            else:
                current["enabled"] = not current.get("enabled", False)
            client.user_reaction_settings[user_id] = current
            save_settings("user_reaction_settings", client.user_reaction_settings)
            status = "enabled" if current["enabled"] else "disabled"
            await interaction.response.send_message(f"Your emotion reactions are now {status}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
    return _toggle

def set_custom_emojis_command(client):
    @app_commands.command(
        name="setemotionemojis",
        description="Set custom emojis for an emotion on this server (admin only)"
    )
    @app_commands.describe(
        emotion="Emotion to set emojis for",
        emojis="Comma-separated list of 3 emojis, e.g. 🙂,😄,😁"
    )
    @app_commands.choices(emotion=emotion_choices)
    async def _set_emojis(interaction: Interaction, emotion: str, emojis: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
            return

        emoji_list = [e.strip() for e in emojis.split(",")]
        if len(emoji_list) != 3:
            await interaction.response.send_message("Please provide exactly 3 emojis separated by commas.", ephemeral=True)
            return

        guild_id = str(interaction.guild_id)
        if not hasattr(client, "guild_emoji_settings"):
            client.guild_emoji_settings = load_settings("guild_emoji_settings") or {}

        if guild_id not in client.guild_emoji_settings:
            client.guild_emoji_settings[guild_id] = {}

        client.guild_emoji_settings[guild_id][emotion] = emoji_list
        save_settings("guild_emoji_settings", client.guild_emoji_settings)

        await interaction.response.send_message(f"Set custom emojis for {emotion} to: {', '.join(emoji_list)}", ephemeral=True)

    return _set_emojis

def reset_emojis_command(client):
    @app_commands.command(
        name="resetemotionemojis",
        description="Reset custom emojis for an emotion on this server to default (admin only)"
    )
    @app_commands.describe(
        emotion="Emotion to reset emojis for"
    )
    @app_commands.choices(emotion=emotion_choices)
    async def _reset_emojis(interaction: Interaction, emotion: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
            return

        guild_id = str(interaction.guild_id)
        if not hasattr(client, "guild_emoji_settings"):
            client.guild_emoji_settings = load_settings("guild_emoji_settings") or {}

        if guild_id in client.guild_emoji_settings and emotion in client.guild_emoji_settings[guild_id]:
            del client.guild_emoji_settings[guild_id][emotion]
            if not client.guild_emoji_settings[guild_id]:
                del client.guild_emoji_settings[guild_id]

            save_settings("guild_emoji_settings", client.guild_emoji_settings)
            await interaction.response.send_message(f"Custom emojis for {emotion} have been reset to default.", ephemeral=True)
        else:
            await interaction.response.send_message(f"No custom emojis set for {emotion} on this server.", ephemeral=True)

    return _reset_emojis

def set_reaction_chance_command(client):
    @app_commands.command(
        name="setreactionchance",
        description="Set the percentage chance the bot will react to your messages"
    )
    @app_commands.describe(
        chance="Chance from 1 to 100 percent"
    )
    async def _set_chance(interaction: Interaction, chance: int):
        if chance < 1 or chance > 100:
            await interaction.response.send_message("Please provide a value between 1 and 100.", ephemeral=True)
            return

        user_id = str(interaction.user.id)
        current = client.user_reaction_settings.get(user_id, {"enabled": True, "reaction_chance": 100})

        if isinstance(current, bool):
            current = {"enabled": current, "reaction_chance": chance}
        else:
            current["reaction_chance"] = chance

        client.user_reaction_settings[user_id] = current
        save_settings("user_reaction_settings", client.user_reaction_settings)

        await interaction.response.send_message(f"Reaction chance set to {chance}%.", ephemeral=True)

    return _set_chance
