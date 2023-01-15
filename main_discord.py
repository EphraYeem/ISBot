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


from discord import Client, Interaction, Intents, app_commands, Object, ButtonStyle
from discord.ui import View, Button

MAX_COMPONENTS = 5

intents = Intents.default()
client = Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name = "yee", description = "My first application Command", guild=Object(id=342412466602639372)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    print(Button["InteractionRoles"])
    print(type(Button["InteractionRoles"]))
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    await tree.sync(guild=Object(id=342412466602639372))
    print(f"Logged in as {client.user}!")  # This is a bad habit. use .format instead.
    v = View()
    v.add_item(Button(style=ButtonStyle.primary, label='yee'))
    await client.get_channel(376343682728853506).send("bot is online", view=v)  # Magic
    # await bot.get_channel(376343682728853506).send("Buttons!", components=[ActionRow(Button(label="The Button", custom_id="button1"))])  # Magic, Also maybe split the line into several lines? it's a bit long.


# @bot.command(aliases=['addi'], help='gets an institution name, emoji that represents it and department_list of the existing departments from the department table (separeted with a comma)')
# @commands.has_role('GOD')
# async def add_institution(ctx, institution_name, emoji, deparment_list):
#     # Validates all departments
#     for dep in deparment_list.split(','):  # Put the validation in it's own function, maybe in a utils module? ehm ehm
#         if not get(ctx.guild.roles, name=dep):
#             await ctx.send(f'Could not found a role with the name {dep}')
#             return
#     # Creates the roles and inserts the info about them to the DB
#     dbcon = sqlite3.connect('IS.db')
#     institution_role = await ctx.guild.create_role(name=institution_name)
#     dbcon.execute(f"INSERT INTO institutions (id, name, matching_emoji) VALUES ({institution_role.id}, '{institution_role.name}', '{emoji}')")
#     dbcon.commit()
#     for dep in deparment_list.split(','):
#         if get(ctx.guild.roles, name=dep):
#             curr_inst_dep_role = await ctx.guild.create_role(name=institution_name + "-" + dep)
#             curr_dep_role = get(ctx.guild.roles, name=dep)
#             dbcon.execute(f"INSERT INTO departments_in_institutions (id, name, institution_id, department_id) VALUES ({curr_inst_dep_role.id}, '{curr_inst_dep_role.name}', {institution_role.id}, {curr_dep_role.id})")
#             dbcon.commit()

#     dbcon.close()

#     category = await ctx.guild.create_category(institution_name)
#     # only institution can see their category
#     await category.set_permissions(ctx.guild.default_role, view_channel=False)
#     await category.set_permissions(institution_role, view_channel=True)

#     # add channel for choose department
#     choose_department_channel = await ctx.guild.create_text_channel('choose-department', category=category)
#     await choose_department_channel.send('Please choose your department', components=generate_components(institution_name))

#     # create general text channel and general voice channel
#     text_general = await ctx.guild.create_text_channel('general-text', category=category)
#     voice_general = await ctx.guild.create_voice_channel('general-talk', category=category)
#     # only institution can see their general *text chat* and voice
#     await text_general.set_permissions(ctx.guild.default_role, view_channel=False)
#     await text_general.set_permissions(institution_role, view_channel=True)
#     # only institution can see their general text chat and *voice*
#     await voice_general.set_permissions(ctx.guild.default_role, view_channel=False)
#     await voice_general.set_permissions(institution_role, view_channel=True)

#     # text and voice channels for every department in the institution
#     for dep in deparment_list.split(','):
#         role_name = institution_name + "-" + dep
#         curr_dep_role = get(ctx.guild.roles, name=role_name)
#         overwrites = {
#             ctx.guild.default_role: PermissionOverwrite(view_channel=False),
#             curr_dep_role: PermissionOverwrite(view_channel=True)
#         }
#         await ctx.guild.create_text_channel(dep, category=category,overwrites=overwrites)
#         await ctx.guild.create_voice_channel(dep, category=category,overwrites=overwrites)

#     # Updates the old choose-institution message - it finds the channel, deletes the old one, and generates a new one
#     choose_institution_channel = get(ctx.guild.channels, name='choose-institution')
#     await choose_institution_channel.purge()
#     await choose_institution_channel.send('ברוכים הבאים לשרת! בחרו את מוסד הלימודים שלכם', components=generate_components())

#     await ctx.send('yee and yeeer <:yee:366667220312522763>')


# @bot.command(aliases=['addd'], help='gets a department name, emoji that represents it and institution_list of the existing institutions from the institution table (separeted with a comma)')
# @commands.has_role('GOD')
# async def add_department(ctx, department_name, emoji, institution_list=None):
#     """"generate new department for existing institution
#     the function get department_name,emoji,list_of_(existing)_institutions_that_has_this_department """
#     # Validates all institution
#     if institution_list:
#         for inst in institution_list.split(','):
#             if not get(ctx.guild.roles, name=inst):
#                 await ctx.send(f'Could not found a role with the name {inst}')
#                 return

#     dbcon = sqlite3.connect('IS.db')
    
#     # Checks if the department exists and Creates a role for department if not
#     if not (dep_role := get(ctx.guild.roles, name=department_name)):
#         dep_role = await ctx.guild.create_role(name=department_name)
#         dbcon.execute(f"INSERT INTO departments (id, name, matching_emoji) VALUES ({dep_role.id}, '{dep_role.name}', '{emoji}')")
    
#     # Creates institutions-specific channels and everything related if an institution list was given
#     if institution_list:
#         for inst in institution_list.split(','):
#             # new dep role for every inst in the list
#             curr_inst_dep_role = await ctx.guild.create_role(name=inst + "-" + department_name)
#             curr_inst_role = get(ctx.guild.roles, name=inst)

#             # Inserts to dii table with specific inst
#             dbcon.execute(f"INSERT INTO departments_in_institutions (id, name, institution_id, department_id) VALUES ({curr_inst_dep_role.id}, '{curr_inst_dep_role.name}', {curr_inst_role.id}, {dep_role.id})")
#             dbcon.commit()

#             # Creates text channels and voice channels for departments in the appropriate institutions categories
#             # and update (deletes and sends a new one) the departments messages (with the button)
#             institution_category = get(ctx.guild.categories, name=inst)
#             role_name = inst + "-" + department_name
#             curr_dep_role = get(ctx.guild.roles, name=role_name)
#             overwrites = {
#                 ctx.guild.default_role: PermissionOverwrite(view_channel=False),
#                 curr_dep_role: PermissionOverwrite(view_channel=True)
#             }
#             await ctx.guild.create_text_channel(department_name, category=institution_category,overwrites=overwrites)
#             await ctx.guild.create_voice_channel(department_name, category=institution_category,overwrites=overwrites)
            
#             # Updates the old choose-institution message - it finds the channel, deletes the old one, and generates a new one
#             choose_department_channel = get(institution_category.channels, name='choose-department')
#             await choose_department_channel.purge()
#             await choose_department_channel.send('Please select your department from the buttons below:', components=generate_components(inst))

#     dbcon.commit()
#     dbcon.close()
#     await ctx.send('yee and yeeer <:yee:366667220312522763>')


# @bot.command(aliases=['gim'], help='generates and sends the message with the institutions buttons roles')
# @commands.has_role('GOD')
# async def generate_institution_message(ctx):
#     await ctx.send('ברוכים הבאים לשרת! בחרו את מוסד הלימודים שלכם', components=generate_components())


# @bot.command(aliases=['gdm'], help='generates and sends the message with the departments (of given institution) buttons roles')
# @commands.has_role('GOD')
# async def generate_dii_message(ctx, institution):
#     await ctx.send('Please select your department from the buttons below:', components=generate_components(institution))


# @bot.event
# async def on_button_click(interaction):
#     """handler function for all buttons click
#     every button generated have the id of the role it represents
#     the function checks by the id if the user that pressed the button have that role or not (gives it if not and takes it if the user have it)
#     """
#     role = get(interaction.guild.roles, id=int(interaction.custom_id))
#     if role not in interaction.user.roles:
#         await interaction.user.add_roles(role)
#         added_flag = True
#     else:
#         await interaction.user.remove_roles(role)
#         added_flag = False
#     # We want to add the department role for those who have the department-in-institution role
#     dbcon = sqlite3.connect('IS.db')
#     dbcon.row_factory = sqlite3.Row  # So we can select the results like a dict
#     if query_results := dbcon.execute(f"select department_id from departments_in_institutions where id = {interaction.custom_id}").fetchone():
#         department_role_id = query_results['department_id']
#         department_role = get(interaction.guild.roles, id=int(department_role_id))
#         if added_flag:
#             await interaction.user.add_roles(department_role)
#         else:
#             await interaction.user.remove_roles(department_role)
#     await interaction.send(content="Congratulations for the role")


# @bot.command(help='gets a name of a role and deletes all the roles that have that name')
# @commands.has_role('GOD')
# async def delrole(ctx, rolename):
#     while role := get(ctx.guild.roles, name=rolename):
#         await role.delete()
#     await ctx.send('deleted them all')


# @bot.command(help='gets a name of a category and deletes all the categories (with theirs sons) that have that name')
# @commands.has_role('GOD')
# async def delcategory(ctx, category_name):
#     while category := get(ctx.guild.categories, name=category_name):
#         for channel in category.channels:
#             await channel.delete()
#         await category.delete()


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


# def generate_components(institution_name=None):
#     """Generate component list for a message.
#     if it wasn't given an institution it genearates an all-institutions buttons
#     if it gets one, it generates the department list for that institution
#     """
#     dbcon = sqlite3.connect('IS.db')
#     dbcon.row_factory = sqlite3.Row  # So we can select the results like a dict
#     if institution_name:
#         roles_query = "SELECT dii.id, d.name, d.matching_emoji FROM departments_in_institutions AS dii JOIN departments AS d on dii.department_id = d.id join institutions AS i on dii.institution_id = i.id WHERE i.name = '{}'".format(institution_name)
#     else:
#         roles_query = "SELECT id, name, matching_emoji FROM institutions"
#     comp_list = dbcon.execute(roles_query).fetchall()
#     components = []
#     curr_action_row = ActionRow()
#     for i, comp in enumerate(comp_list):
#         if i and (i + 1) % MAX_COMPONENTS == 0:
#             components.append(curr_action_row)
#             curr_action_row = ActionRow()
#         curr_action_row.append(Button(label=comp['name'], custom_id=comp['id'], emoji=get_actual_emoji(comp['matching_emoji'])))
#     components.append(curr_action_row)
#     return components


# def get_actual_emoji(emoji):
#     """get a string of emoji
#     if it's a custom emoji (formatted like '<:nick:id>') it extracts the id and return the server emoji object by that id
#     if it's a normal emoji it just returns it
#     """
#     if custom := re.search(r'(?<=:)\d+(?![a-zA-Z])', emoji):
#         return bot.get_emoji(int(custom.group()))
#     else:
#         return emoji


# @bot.command()
# @commands.has_role('GOD')
# async def yee(ctx):
#     i = 1
#     while channel := get(ctx.guild.channels, name=str(i)):
#         await channel.delete()
#         i += 1



client.run('ODkyMDgyNjAyMDY2OTgwOTY0.YVHuqg.tQgbfMKeFFYE2Y3KnRdl1rwKS50')
