from discord.ui import View, Button
from discord import Interaction, Role, ButtonStyle, Embed, Color, Guild
import discord.utils    
import db_mgr


class RoleButton(Button):
        def __init__(self, role: Role, name: str, matching_emoji: str):
            super().__init__(custom_id=str(role.id), label=name, emoji=matching_emoji, style=ButtonStyle.grey)
            #TODO:= change the str(role.id) to just string in the db and cast it before inserting
            self.role = role
        
        async def callback(self, interaction: Interaction):
            try:
                if self.role not in interaction.user.roles:
                    await interaction.user.add_roles(self.role)
                    added_flag = True
                    msg = "Congratulations for the role"
                else:
                    await interaction.user.remove_roles(self.role)
                    added_flag = False
                    msg = "Role removed"
                if (department_in_institution := db_mgr.get_department_from_dii(self.role.id)):
                    department_role = discord.utils.get(interaction.guild.roles, id=int(department_in_institution.department_id))
                    if added_flag:
                        await interaction.user.add_roles(department_role)
                    else:
                        await interaction.user.remove_roles(department_role)
            except Exception as e:
                msg = "Something went wrong, Contact the server administrator"
                print(e)
            await interaction.response.send_message(msg, ephemeral=True)


def get_institutions_roles(guild: Guild):
    roles_view = View()
    for inst in db_mgr.get_institutions():
        if inst_role := discord.utils.get(guild.roles, id=inst.id):
            roles_view.add_item(RoleButton(inst_role, inst.name, inst.matching_emoji)) 
    return roles_view


def get_departments_roles(guild: Guild, institution: str):
    roles_view = View()
    for dept_in_inst in db_mgr.get_departments(institution):
        if dept_in_inst_role := discord.utils.get(guild.roles, id=dept_in_inst.id):
            roles_view.add_item(RoleButton(dept_in_inst_role, dept_in_inst.name, dept_in_inst.matching_emoji)) 
    return roles_view
