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

bot = discord.ext.commands.Bot(command_prefix=data["prefix"])

@bot.command()
async def role(ctx: discord.ext.commands.Context, name: str, color: discord.ext.commands.ColourConverter):
    print(f"{ctx.author}: {ctx.message.content}")
    async with ctx.typing():
        if len(ctx.author.roles) > 1:
            await ctx.author.top_role.edit(color=color, name=name, hoist=True)
        else:
            await ctx.author.add_roles(await ctx.guild.create_role(color=color, name=name, hoist=True))
        embed = discord.Embed(title=f"Set {ctx.author.name}'s role to \"{name}\" with the color `{color}`")
        embed.color = color
        await ctx.send(embed=embed)

bot.run(data["token"])