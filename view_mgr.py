from discord.ui import View, Button
from discord import Interaction, Role, ButtonStyle, Embed, Color
import discord.utils    
import db_mgr


class RoleButton(Button):
        def __init__(self, role: Role):
            super().__init__(style=ButtonStyle.primary, label=role.name, custom_id=role.id)
            # role = discord.utils.get(interaction.guild.roles, id=id)
            self.role = role
        
        async def callback(self, interaction: Interaction):
            print("wow")
            try:
                await interaction.user.add_roles(self.role)
                embed = Embed(title="role added", description=f"You have been given the role {self.role.name}.", color=Color.green)
            except Exception as e:
                embed = Embed(title="Something went wrong", description=f"Contact the server administrator.", color=Color.red)
                print(e)
            await interaction.response.send_message(embed=embed, ephemeral=True)


class InstitutionsRoles(View):
    def __init__(self, interaction: Interaction):
        super().__init__()
        
        for inst in db_mgr.get_institutions():
            role = discord.utils.get(interaction.guild.roles, id=inst.id)
            if role:
                self.add_item(RoleButton(role)) 


class DepartmentsRoles(View):
    def __init__(self, interaction: Interaction, institution: str):
        super().__init__()

    for dept in db_mgr.get_departments(institution):
        role = discord.utils.get(interaction.guild.roles, id=dept.role_id)
        if role:
            self.add_item(RoleButton(role)) 