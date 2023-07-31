import discord
import asyncio
import configparser
from tabulate import tabulate  # Import tabulate library

from toys import getToys

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

toy_type = eval(config.get("Toy", "type"))  # Use eval to convert the string to a tuple
ratelimit = int(config.get("Toy", "ratelimit"))

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

clientInitiated = False
token = config.get("Discord", "token")
feed_channel_id = int(config.get("Discord", "feed_channel_id"))
release_channel_id = int(config.get("Discord", "release_channel_id"))

# Variable to store the last fetched toys
last_toys = []

@client.event
async def on_ready():
    global last_toys  # Access the global variable within the function
    channel = client.get_channel(feed_channel_id)
    release_channel = client.get_channel(release_channel_id)

    await channel.send("**I am awake once again**, *I will continue monitoring! <3*")
    clientInitiated = True
    print('Client ready!')

    role_id_to_ping = config.get("Special", "ping_toy_role_id")
    role_to_ping = f"<@&{role_id_to_ping}>"

    # List of toy names to match
    ping_toy_names = config.get("Special", "ping_toy_names")

    while True:
        print("Fetching toys... \n")
        toy_types = set(toy_type)  # Convert tuple to set
        toys = getToys(toy_types)
        print("Toys fetched:")
        print(tabulate(toys, headers="firstrow"))  # Print the fetched toys as a table
        print()

        if channel and toys != last_toys:
            print("Toys are different. Sending updates...")
            for toy in toys:
                # Create an embed message
                embed = discord.Embed(title="Toy Details")
                if toy[4]:
                    embed.color = discord.Color.dark_red()
                    embed.add_field(name="Flop", value=toy[4], inline=False)
                    if toy[2]:
                        embed.add_field(name="Discounted Price", value=toy[0] + "$" + " ~~" + toy[2] + "$~~", inline=False)
                    else:
                        embed.add_field(name="Price", value=toy[2] + "$", inline=False)

                else:
                    embed.color = discord.Color.dark_green()
                    if toy[2]:
                        embed.add_field(name="Price", value=toy[2] if toy[2] else "N/A" + "$", inline=False)

                # Add External Flop Reason to the embed
                if toy[5]:
                    embed.add_field(name="External Flop Reason", value=toy[5], inline=False)

                embed.add_field(name="Product Name", value=toy[1].capitalize(), inline=False)
                embed.add_field(name="Color", value=toy[3], inline=False)

                if toy[6]:
                    try:
                        embed.set_image(url=toy[6])
                    except discord.errors.HTTPException as e:
                        print(f"Invalid image URL: {e}")
                        embed.set_image(
                            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/310px-Placeholder_view_vector.svg.png")

                # Check if the toy name matches any in the ping_toy_names list
                if toy[1].upper() in ping_toy_names:
                    # Create an embed message
                    await release_channel.send(f"{role_to_ping}")
                    embed2 = discord.Embed(title=f"{toy[1].capitalize()} ** is available for** " + toy[0] + "$!")
                    embed2.color = discord.Color.blurple()
                    embed2.add_field(name="Product Name", value=toy[1].capitalize(), inline=False)
                    embed2.add_field(name="Color", value=toy[3], inline=False)

                    if toy[4]:
                        embed2.color = discord.Color.dark_red()
                        embed2.add_field(name="Flop", value=toy[4], inline=False)
                        if toy[2]:
                            embed2.add_field(name="Discounted Price", value=toy[0] + "$" + " ~~" + toy[2] + "$~~", inline=False)
                        else:
                            embed2.add_field(name="Price", value=toy[2] + "$", inline=False)
                    if toy[6]:
                        try:
                            embed2.set_image(url=toy[6])
                        except discord.errors.HTTPException as e:
                            print(f"Invalid image URL: {e}")
                            embed2.set_image(
                                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/310px-Placeholder_view_vector.svg.png")
                    
                    await release_channel.send(embed=embed2)
                
                # Send the embed message
                await channel.send(embed=embed)

            await channel.send("**These were all the toys I found this time**, *thanks for checking in! <3*")
        else:
            print("Toys are the same. Skipping updates. \n")

        await asyncio.sleep(ratelimit)
        print("Sleeping.")


def startClient():
    client.run(token)
