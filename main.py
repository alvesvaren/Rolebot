import json
import discord
import discord.ext.commands

data = {
    "token": "",
    "prefix": "!"
}

try:
    with open("config.json") as file:
        data = json.load(file)
except FileNotFoundError:
    with open("config.json", "w") as file:
        json.dump(data, file, indent=4)
        print("Created default config file. Modify it and run the program again")

bot = discord.ext.commands.Bot(command_prefix=data["prefix"])

@bot.command()
async def test(ctx):
    pass

bot.run(data["token"])