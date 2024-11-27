from time import sleep
import bloxflip
import discord
import random
from discord import app_commands 

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False  # Flag to check if commands are synced

    async def on_ready(self):
        await self.wait_until_ready()  # Wait until the client is ready
        if not self.synced: 
            await tree.sync()  # Sync the command tree with Discord
            self.synced = True
        print(f"We have logged in as {self.user}.")  # Log the bot's username

client = aclient()
tree = app_commands.CommandTree(client)  # Create a command tree for the bot


@tree.command(name = 'mines', description='auto player mines') 
async def self(interaction: discord.Interaction, bet_amount : int, mine_amount : int, auth_token : str):
    # Check if the bet amount is valid
    if bet_amount < 5:
        await interaction.response.send_message("bet amount must be higher than 5!")  # Notify user of invalid bet amount
        return 0
    try:
        # Start a new mines game with the specified bet amount and number of mines
        start_game = bloxflip.Mines.Create(betamount=bet_amount, mines=mine_amount, auth=auth_token)  
        if start_game.status_code == 400:
            await interaction.response.send_message("Failed to start game | Bet amount prob higher than balance")  # Handle insufficient balance
            return 0
        await interaction.response.send_message("Game started! use /choose_mine to click a mine")  # Notify user that the game has started
    except:
        await interaction.response.send_message("Error of the following: Bet amount, Mine amount, Auth token, api did not respond")  # Handle errors

@tree.command(name = 'choose_mine', description='choose how many mines u want to click') 
async def self(interaction: discord.Interaction, mine_amount : int, auth_token : str):
    try:
        # Check the user's balance using the provided auth token
        bloxflip.Currency.Balance(auth=auth_token)  
    except:
        await interaction.response.send_message("invalid auth token")  # Handle invalid auth token
        return 0
    times = range(mine_amount)  # Create a range for the number of mines to click
    await interaction.response.send_message('Clicking mines...')  # Notify user that mines are being clicked
    try:
        for x in times:
            try:
                # Randomly select a mine to click
                a = random.randint(0, 24)  
                bloxflip.Mines.Choose(choice=int(a), auth=auth_token)  # Click the selected mine
                await interaction.followup.send('clicked mine')  # Notify user of successful click
            except:
                await interaction.followup.send("failed to click mines")  # Handle click failure
                return
        
    except:
        await interaction.followup.send("failed to click mines")  # Handle errors during clicking

@tree.command(name='cashout', description='cashout of a mines game')
async def self(interaction: discord.Interaction, auth_token : str):
    try:
        # Check the user's balance using the provided auth token
        bloxflip.Currency.Balance(auth=auth_token)  
    except:
        await interaction.response.send_message("invalid auth token")  # Handle invalid auth token
        return 0
    await interaction.response.send_message("cashing out of mines game")  # Notify user of cashout
    try:
        # Cash out from the mines game
        bloxflip.Mines.Cashout(auth=auth_token)  
        await interaction.followup.send("Cashed out of game!")  # Notify user of successful cashout
    except:
        await interaction.followup.send("not in a game")  # Handle case where user is not in a game
    

client.run('bot token here')  # Run the bot with the specified token
