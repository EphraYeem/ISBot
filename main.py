import sqlite3

from discord_components import ComponentsBot, Button, ActionRow
from discord.utils import get
from discord.ext import commands

bot = ComponentsBot("$")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    await bot.get_channel(376343682728853506).send("bot is online")
    await bot.get_channel(376343682728853506).send("Buttons!", components=[ActionRow(Button(label="The Button", custom_id="button1"))])

@bot.event
async def on_button_click(interaction):
    role = get(interaction.guild.roles, id=893447856097226783)
    if role not in interaction.user.roles:
        await interaction.user.add_roles(role)
    else:
        await interaction.user.remove_roles(role)
    await interaction.send(content="Congratulations for the role")

@bot.command(help='gets an institution name, emoji that represents it and department_list of the existing departments from the department table (separeted with a comma)')
@commands.has_role('GOD')
async def add_institution(ctx, name, emoji, deparment_list=None):
    # Validates all departments
    for dep in deparment_list.split(','):
        if not get(ctx.guild.roles, name=dep):
            await ctx.send(f'Could not found a role with the name {dep}')
            return
    # Creates the roles and inserts the info about them to the DB
    dbcon = sqlite3.connect('IS.db')
    institution_role = await ctx.guild.create_role(name=name)
    dbcon.execute(f"INSERT INTO institutions (id, name, matching_emoji) VALUES ({institution_role.id}, '{institution_role.name}', '{emoji}')")
    dbcon.commit()
    if deparment_list:
        for dep in deparment_list.split(','):
            if get(ctx.guild.roles, name=dep):
                curr_inst_dep_role = await ctx.guild.create_role(name=name + "-" + dep)
                curr_dep_role = get(ctx.guild.roles, name=dep)
                dbcon.execute(f"INSERT INTO departments_in_institutions (id, name, institution_id, department_id) VALUES ({curr_inst_dep_role.id}, '{curr_inst_dep_role.name}', {institution_role.id}, {curr_dep_role.id})")
                dbcon.commit()
    
    dbcon.close()
    await ctx.send('yee and yeeer <:yee:366667220312522763>')

@bot.command(aliases=['gim'], help='generates and sends the message with the institutions buttons roles')
@commands.has_role('GOD')
async def generate_institution_message(ctx):
    dbcon = sqlite3.connect('IS.db')
    
    await ctx.send('yee')


bot.run('sike')
