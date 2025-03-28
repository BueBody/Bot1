import os
import discord

# Устанавливаем нужные intents
intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

# Событие, когда бот подключается к серверу
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Событие для обработки сообщений
@client.event
async def on_message(message):
    if message.content.startswith("!hello"):
        await message.channel.send(f"Hello, {message.author.name}!")

# Используем переменную окружения для токена
client.run(os.getenv('DISCORD_TOKEN'))
