import discord
import os

# Токен не должен быть здесь, он будет получен из переменных окружения
token = os.getenv('YOUR_BOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run(token)