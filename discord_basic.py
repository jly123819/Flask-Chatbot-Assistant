import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}! 👋")

@bot.command(name='recipe', help='Searches for a recipe using the custom Flask API. Usage: !recipe <dish name>')
async def find_recipe(ctx, *, dish_name: str):
    """Fetches recipe data from the Flask backend and splits long messages."""

    payload = {"message": dish_name}
    await ctx.send(f"Asking the recipe backend about '{dish_name}'...")

    try:
        response = requests.post("https://flask-chatbot-457918.ue.r.appspot.com/chat", json=payload)
        response.raise_for_status()
        api_data = response.json()
        recipe_response = api_data.get("response")

        if recipe_response:
            processed_response = recipe_response.replace('\\n', '\n')
            print(f"Bot repr after replace: {repr(processed_response)}") 

            max_chars = 2000
            if len(processed_response) <= max_chars:
                print(f"Bot repr before send (full): {repr(processed_response)}") 
                await ctx.send(processed_response)
            else:
                print(f"Response length ({len(processed_response)}) exceeds {max_chars}. Splitting message.")
                start = 0
                while start < len(processed_response):
                    chunk = processed_response[start:start + max_chars]
                    print(f"Bot repr before send (chunk): {repr(chunk)}") 
                    await ctx.send(chunk)
                    start += max_chars
        else:
            await ctx.send("Sorry, I received an unexpected empty response from the recipe backend.")


    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Flask API: {e}")
        await ctx.send("Sorry, I couldn't connect to the recipe backend service. Please make sure it's running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if "error code: 50035" in str(e):
             await ctx.send("Tried to send a message that was too long, even after attempting to split. Please report this.")
        else:
             await ctx.send("An unexpected error occurred while processing the recipe.")

@bot.event
async def on_command_error(ctx, error):
    """Handles errors raised during command invocation."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Uh-oh {ctx.author.name}, I don't know that command! Try `!hello` or `!recipe <dish name>`.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Oops! You missed a required argument for the `{ctx.command.name}` command.")
    elif isinstance(error, commands.CommandInvokeError):
        print(f"Error invoking command {ctx.command.name}: {error.original}")
        if not isinstance(error.original, requests.exceptions.RequestException):
             await ctx.send("An error occurred while running the command.")
    else:
        print(f'Unhandled command error: {error}')
        await ctx.send("An unexpected error occurred.")

bot.run('MTM2ODcyNDIzNDI1MTI3MjIxMg.G-vzxL.gmACRDMhRhUdpave12ZfhAQsYN2MI6hTVXYNjo')
