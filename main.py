import json
import discord
import discord.ext.commands
import asyncio

data = {
    "token": "",
    "prefix": "!",
    "blacklisted_roles": ["Server Booster", "@everyone", "everyone"]
}

color_converter = discord.ext.commands.ColourConverter()

try:
    with open("config.json") as file:
        data = json.load(file)
except FileNotFoundError:
    with open("config.json", "w") as file:
        json.dump(data, file, indent=4)
        print("Created default config file. Modify it and run the program again")
        quit()

bot = discord.ext.commands.Bot(command_prefix=data["prefix"])


def get_highest_editable_role(member: discord.Member, me: discord.Member) -> discord.Role:
    highest_avalible_role: discord.Role = None
    for role in member.roles:
        if role.position < me.top_role.position and (highest_avalible_role == None or role.position > highest_avalible_role.position) and not role.name in data["blacklisted_roles"]:
            highest_avalible_role = role
    return highest_avalible_role


@bot.command()
async def role(ctx: discord.ext.commands.Context, name: str = None, color: discord.ext.commands.ColourConverter = None):
    print(f"{ctx.author}: {ctx.message.content}")
    role = get_highest_editable_role(ctx.author, ctx.me)
    if not color:
        if role:
            color = role.color
        else:
            color = ctx.author.top_role.color  # gets @everyone and the default color (#000000)
    async with ctx.typing():
        # if this is not here it continues "typing" after done
        await asyncio.sleep(0.1)
        if name:
            if name in data["blacklisted_roles"]:
                await ctx.send("That name is not allowed! Please choose another one instead.")
                return
            if role:
                await role.edit(color=color, name=name, hoist=True)
            else:
                await ctx.author.add_roles(await ctx.guild.create_role(color=color, name=name, hoist=True))
            embed = discord.Embed(
                title=f"Set {ctx.author.display_name}'s role to \"{name}\" with the color `{color}`")
            embed.color = color
            await ctx.send(embed=embed)
        else:
            if role:
                embed = discord.Embed(
                    title=f"Your role name is \"{role.name}\" and has the color `{role.color}`")
                embed.color = role.color
                await ctx.send(embed=embed)
            else:
                await ctx.send("It looks like you need to set a role first. Try `!role \"role name\" #789abc`")

bot.run(data["token"])
