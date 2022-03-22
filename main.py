import nextcord
from nextcord.ext import commands
import json
import requests
import colorama
from colorama import Fore

    

colorama.init()

with open('./config.json') as f:
    global data
    global token
    global prefix
    global VerifiedRole
    data = json.load(f)
    token = data["TOKEN"]
    prefix = data["PREFIX"]
    VerifiedRole = data["VERIFIEDROLE"]
    if prefix == "":
        print(Fore.RED + "[BOT] - No prefix is set. Exiting.")
        exit()
    else:
        print(Fore.LIGHTGREEN_EX + f"[BOT] - Prefix: {prefix}\n")

    if VerifiedRole == "":
        print(Fore.RED + "[BOT] - No Role is set. Exiting.")
        exit()
    else:
        print(Fore.LIGHTGREEN_EX + f"[BOT] - Verified Role: {VerifiedRole}\n")




client = commands.Bot(command_prefix=prefix)
client.remove_command('help')

if token == "":
    print(Fore.RED + "[BOT] - No Token is set. Exiting.")
    exit()
else:
    print(Fore.LIGHTGREEN_EX + f"[BOT] - Logged in. \n")

@client.event
async def on_ready():
    print(Fore.CYAN + "[BOT] - Started running.")

class V(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label = "Rover", style=nextcord.ButtonStyle.danger)
    async def rover(self, button: nextcord.ui.Button, inter: nextcord.Interaction):
        body = requests.get(f'https://verify.eryn.io/api/user/{inter.user.id}')
        data = body.json()
        status = data["status"]
        if status == "ok":
            robloxUser = data["robloxUsername"]
            robloxId = data["robloxId"]
            await inter.response.send_message(f'Welcome, {robloxUser} ({robloxId}) to {inter.guild.name}.',ephemeral=True)
            role = nextcord.utils.get(inter.guild.roles,name=VerifiedRole)
            await inter.user.edit(nick=robloxUser)
            if nextcord.errors.Forbidden:
                await inter.edit_original_message('Could not name you, could you please give me a higher role?')
            if role in inter.user.roles:
                await inter.edit_original_message(f'Error: You already have this role..')
            else:
                await inter.user.add_roles(role)
        elif status == "error":
            await inter.response.send_message(f'Error 500 - You could not be verified with Rover.',ephemeral=True)
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "Bloxlink", style=nextcord.ButtonStyle.danger)
    async def bloxlink(self, button: nextcord.ui.Button, inter: nextcord.Interaction):
        body = requests.get(f'https://api.blox.link/v1/user/{inter.user.id}')
        data = body.json()
        status = data["status"]
        if status == "ok":
            robloxId = data["primaryAccount"]
            body2 = requests.get(f'https://users.roblox.com/v1/users/{robloxId}')
            data2 = body2.json()
            robloxUser = data2["name"]
            await inter.response.send_message(f'Welcome, {robloxUser} ({robloxId}) to {inter.guild.name}.',ephemeral=True)
            role = nextcord.utils.get(inter.guild.roles,name=VerifiedRole)
            await inter.user.edit(nick=robloxUser)
            if nextcord.errors.Forbidden:
                await inter.edit_original_message('Could not name you, could you please give me a higher role?')
            if role in inter.user.roles:
                await inter.edit_original_message(f'Error: You already have this role..')
            else:
                await inter.user.add_roles(role)
        elif status == "error":
            await inter.response.send_message(f'Error 500 - You could not be verified with Bloxlink.',ephemeral=True)
        self.value = True
        self.stop()



@client.command()
async def setup(ctx):
    view = V()
    verifEmbed = nextcord.Embed(title="Verification",description=f"Welcome to {ctx.guild.name}.\n\nBefore we can verify you, you will have to verify yourself via the **Bloxlink** or **Rover** API.\n\nIf you encounter issues with this verification system, please contact a staff member.\nOther than that, please have a pleasant stay.",color=nextcord.Color.og_blurple())
    await ctx.send(embed=verifEmbed,view=view)
    


client.run(token)
