import json
import discord
import discord.ext.commands

data = {
    "token": "",
    "prefix": "!"
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

@bot.command()
async def role(ctx: discord.ext.commands.Context, name: str = None, color: discord.ext.commands.ColourConverter = None):
    print(f"{ctx.author}: {ctx.message.content}")
    if not color:
        color = ctx.author.top_role.color
    async with ctx.typing():
        if name:
            if len(ctx.author.roles) > 1:
                await ctx.author.top_role.edit(color=color, name=name, hoist=True)
            else:
                await ctx.author.add_roles(await ctx.guild.create_role(color=color, name=name, hoist=True))
            embed = discord.Embed(title=f"Set {ctx.author.name}'s role to \"{name}\" with the color `{color}`")
            embed.color = color
            await ctx.send(embed=embed)
        else:
            if len(ctx.author.roles) > 1:
                embed = discord.Embed(title=f"Your role name is \"{ctx.author.top_role.name}\" and has the color `{ctx.author.top_role.color}`")
                embed.color = ctx.author.top_role.color
                await ctx.send(embed=embed)
            else:
                await ctx.send("It looks like you need to set a role first. Try `!role \"role name\" #789abc`")

bot.run(data["token"])