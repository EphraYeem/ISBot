##### SEPERATE TO DIFFERENT FILES
#### Consts.py(!)
##### Messages.py (!)
##### Docstrings?
##### class SQLmanager.

# import re
# import sqlite3

# from discord import PermissionOverwrite
# from discord_components import ComponentsBot, Button, ActionRow
# from discord.utils import get
# from discord.ext import commands


from discord import Client, Interaction, Intents, app_commands, Object, ButtonStyle, PermissionOverwrite
from discord.ui import View, Button
from discord.utils import get
from view_mgr import get_institutions_roles, get_departments_roles
import db_mgr

#TODO: add exception handling for db and everything

MAX_COMPONENTS = 5

intents = Intents.default()
client = Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name = "yee", guild=Object(id=342412466602639372), description = "My first application Command") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.checks.has_role('GOD')
async def first_command(interaction: Interaction):
    await interaction.response.send_message("Hello!")


@client.event
async def on_ready():
    israeli_students_guild = get(client.guilds, id=342412466602639372)
    await tree.sync(guild=israeli_students_guild)
    print(f"Logged in as {client.user}!")  # This is a bad habit. use .format instead.
    await client.get_channel(376343682728853506).send("bot is online", view=get_institutions_roles(israeli_students_guild))  # Magic


#TODO: write shorter description and check if department_list can be default None
#gets an institution name, emoji that represents it and department_list of the existing departments from the department table (separeted with a comma)
@tree.command(name="add_institution", guild=Object(id=342412466602639372),  description='beseder')
@app_commands.checks.has_role('GOD')
async def add_institution(interaction: Interaction, institution_name: str, emoji: str, department_list: str):
    await interaction.response.defer()
    # Validates all departments
    for dep in department_list.split(','):  # Put the validation in it's own function, maybe in a utils module? ehm ehm
        if not get(interaction.guild.roles, name=dep):
            await interaction.response.send_message(f'Could not found a role with the name {dep}')
            return
    # Creates the roles and inserts the info about them to the DB
    # dbcon = sqlite3.connect('IS.db')
    institution_role = await interaction.guild.create_role(name=institution_name)
    db_mgr.insert_institution(institution_role.id, institution_role.name, emoji)
    # dbcon.execute(f"INSERT INTO institutions (id, name, matching_emoji) VALUES ({institution_role.id}, '{institution_role.name}', '{emoji}')")
    # dbcon.commit()
    for dep in department_list.split(','):
        if get(interaction.guild.roles, name=dep):
            curr_inst_dep_role = await interaction.guild.create_role(name=institution_name + "-" + dep)
            #TODO: walrus
            curr_dep_role = get(interaction.guild.roles, name=dep)
            db_mgr.insert_department_in_institution(curr_inst_dep_role.id, curr_inst_dep_role.name, institution_role.id, curr_dep_role.id)
            # dbcon.execute(f"INSERT INTO departments_in_institutions (id, name, institution_id, department_id) VALUES ({curr_inst_dep_role.id}, '{curr_inst_dep_role.name}', {institution_role.id}, {curr_dep_role.id})")
            # dbcon.commit()

    # dbcon.close()

    category = await interaction.guild.create_category(institution_name)
    # only institution can see their category
    await category.set_permissions(interaction.guild.default_role, view_channel=False)
    await category.set_permissions(institution_role, view_channel=True)

    # add channel for choose department
    choose_department_channel = await interaction.guild.create_text_channel('choose-department', category=category)
    # await choose_department_channel.send('Please choose your department', components=generate_components(institution_name))
    await choose_department_channel.send('Please choose your department', view=get_departments_roles(interaction.guild, institution_name))


    # create general text channel and general voice channel
    text_general = await interaction.guild.create_text_channel('general-text', category=category)
    voice_general = await interaction.guild.create_voice_channel('general-talk', category=category)
    # only institution can see their general *text chat* and voice
    await text_general.set_permissions(interaction.guild.default_role, view_channel=False)
    await text_general.set_permissions(institution_role, view_channel=True)
    # only institution can see their general text chat and *voice*
    await voice_general.set_permissions(interaction.guild.default_role, view_channel=False)
    await voice_general.set_permissions(institution_role, view_channel=True)

    # text and voice channels for every department in the institution
    for dep in department_list.split(','):
        role_name = institution_name + "-" + dep
        curr_dep_role = get(interaction.guild.roles, name=role_name)
        overwrites = {
            interaction.guild.default_role: PermissionOverwrite(view_channel=False),
            curr_dep_role: PermissionOverwrite(view_channel=True)
        }
        await interaction.guild.create_text_channel(dep, category=category,overwrites=overwrites)
        await interaction.guild.create_voice_channel(dep, category=category,overwrites=overwrites)

    # Updates the old choose-institution message - it finds the channel, deletes the old one, and generates a new one
    choose_institution_channel = get(interaction.guild.channels, name='choose-institution')
    await choose_institution_channel.purge()
    # await choose_institution_channel.send('ברוכים הבאים לשרת! בחרו את מוסד הלימודים שלכם', components=generate_components())
    await choose_institution_channel.send('ברוכים הבאים לשרת! בחרו את מוסד הלימודים שלכם', view=get_institutions_roles(interaction.guild))

    await interaction.followup.send('yee and yeeer <:yee:366667220312522763>')


#gets a department name, emoji that represents it and institution_list of the existing institutions from the institution table (separeted with a comma)
@tree.command(name="add_department", guild=Object(id=342412466602639372), description='beseder')
@app_commands.checks.has_role('GOD')
async def add_department(interaction: Interaction, department_name: str, emoji: str, institution_list: str=None):
    """"generate new department for existing institution
    the function get department_name,emoji,list_of_(existing)_institutions_that_has_this_department """
    await interaction.response.defer()
    # Validates all institution
    if institution_list:
        for inst in institution_list.split(','):
            if not get(interaction.guild.roles, name=inst):
                await interaction.response.send_message(f'Could not found a role with the name {inst}')
                return

    # dbcon = sqlite3.connect('IS.db')
    
    # Checks if the department exists and Creates a role for department if not
    if not (dep_role := get(interaction.guild.roles, name=department_name)):
        dep_role = await interaction.guild.create_role(name=department_name)
        db_mgr.insert_department(dep_role.id, dep_role.name, emoji)
        # dbcon.execute(f"INSERT INTO departments (id, name, matching_emoji) VALUES ({dep_role.id}, '{dep_role.name}', '{emoji}')")
    
    # Creates institutions-specific channels and everything related if an institution list was given
    if institution_list:
        for inst in institution_list.split(','):
            # new dep role for every inst in the list
            curr_inst_dep_role = await interaction.guild.create_role(name=inst + "-" + department_name)
            curr_inst_role = get(interaction.guild.roles, name=inst)

            # Inserts to dii table with specific inst
            db_mgr.insert_department_in_institution(curr_inst_dep_role.id, curr_inst_dep_role.name, curr_inst_role.id, dep_role.id)
            # dbcon.execute(f"INSERT INTO departments_in_institutions (id, name, institution_id, department_id) VALUES ({curr_inst_dep_role.id}, '{curr_inst_dep_role.name}', {curr_inst_role.id}, {dep_role.id})")
            # dbcon.commit()

            # Creates text channels and voice channels for departments in the appropriate institutions categories
            # and update (deletes and sends a new one) the departments messages (with the button)
            institution_category = get(interaction.guild.categories, name=inst)
            role_name = inst + "-" + department_name
            curr_dep_role = get(interaction.guild.roles, name=role_name)
            overwrites = {
                interaction.guild.default_role: PermissionOverwrite(view_channel=False),
                curr_dep_role: PermissionOverwrite(view_channel=True)
            }
            await interaction.guild.create_text_channel(department_name, category=institution_category,overwrites=overwrites)
            await interaction.guild.create_voice_channel(department_name, category=institution_category,overwrites=overwrites)
            
            # Updates the old choose-institution message - it finds the channel, deletes the old one, and generates a new one
            choose_department_channel = get(institution_category.channels, name='choose-department')
            await choose_department_channel.purge()
            await choose_department_channel.send('Please select your department from the buttons below:', view=get_departments_roles(interaction.guild, inst))
            # await choose_department_channel.send('Please select your department from the buttons below:', components=generate_components(inst))

    # dbcon.commit()
    # dbcon.close()
    await interaction.followup.send('yee and yeeer <:yee:366667220312522763>')


@tree.command(name="generate_institution_message", guild=Object(id=342412466602639372), description='generates and sends the message with the institutions buttons roles')
@app_commands.checks.has_role('GOD')
async def generate_institution_message(interaction: Interaction):
    await interaction.channel.send('ברוכים הבאים לשרת! בחרו את מוסד הלימודים שלכם', view=get_institutions_roles(interaction.guild))


@tree.command(name="generate_dii_message", guild=Object(id=342412466602639372), description='generates and sends the message with the departments (of given institution) buttons roles')
@app_commands.checks.has_role('GOD')
async def generate_dii_message(interaction: Interaction, institution: str):
    await interaction.channel.send('Please select your department from the buttons below:', view=get_departments_roles(interaction.guild, institution))


@tree.command(name="delrole", guild=Object(id=342412466602639372), description='gets a name of a role and deletes all the roles that have that name')
@app_commands.checks.has_role('GOD')
async def delrole(interaction: Interaction, rolename: str):
    while role := get(interaction.guild.roles, name=rolename):
        await role.delete()
    await interaction.response.send_message('deleted them all')


@tree.command(name="delcategory", guild=Object(id=342412466602639372), description='gets a name of a category and deletes all the categories (with theirs sons) that have that name')
@app_commands.checks.has_role('GOD')
async def delcategory(interaction: Interaction, category_name: str):
    while category := get(interaction.guild.categories, name=category_name):
        for channel in category.channels:
            await channel.delete()
        await category.delete()


# @bot.command(help='helper function to get a custom emoji string representation')
# async def emoj(ctx, emoji):
#     await ctx.send(emoji)


# @bot.command(help='deletes all the data from all the tables in the DB and deletes the roles that exists there')
# @commands.has_role('GOD')
# async def clean_db(ctx):
#     role_id_list = []
#     dbcon = sqlite3.connect('IS.db')
#     dbcon.row_factory = sqlite3.Row  # So we can select the results like a dict
#     role_id_list.extend(dbcon.execute("SELECT id FROM institutions").fetchall())
#     role_id_list.extend(dbcon.execute("SELECT id FROM departments").fetchall())
#     role_id_list.extend(dbcon.execute("SELECT id FROM departments_in_institutions").fetchall())
#     for r in role_id_list:
#         await get(ctx.guild.roles, id=r['id']).delete()
#     dbcon.execute('delete from institutions')
#     dbcon.execute('delete from departments')
#     dbcon.execute('delete from departments_in_institutions')
#     dbcon.commit()
#     dbcon.close()
#     await ctx.send('clean af')


# def get_actual_emoji(emoji):
#     """get a string of emoji
#     if it's a custom emoji (formatted like '<:nick:id>') it extracts the id and return the server emoji object by that id
#     if it's a normal emoji it just returns it
#     """
#     if custom := re.search(r'(?<=:)\d+(?![a-zA-Z])', emoji):
#         return bot.get_emoji(int(custom.group()))
#     else:
#         return emoji


client.run('ODkyMDgyNjAyMDY2OTgwOTY0.GwcbYx.IVx0qWUeFR6VpJu12vBV4DeXrZJ3tKCJ_hpAs0')
