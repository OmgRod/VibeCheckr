from discord import app_commands, Interaction
from settings import save_settings

def toggle_reactions(client):
    @app_commands.command(name="togglereactions", description="Toggle automatic emotion reactions on or off for yourself")
    async def _toggle(interaction: Interaction):
        user_id = str(interaction.user.id)
        current = client.user_reaction_settings.get(user_id, False)
        client.user_reaction_settings[user_id] = not current
        save_settings(client.user_reaction_settings)
        status = "enabled" if not current else "disabled"
        await interaction.response.send_message(f"Your emotion reactions are now {status}.", ephemeral=True)
    return _toggle
