import discord
import os
import asyncio
from datetime import datetime
from discord.ext import commands
from discord import Game, Spotify
import pytz

intents = discord.Intents.default()
intents.members = True  # Для отслеживания активности пользователей

client = discord.Client(intents=intents)

# Словарь для хранения времени начала активности
activity_start_time = {}

# Настройка префикса для команд
bot = commands.Bot(command_prefix='/', intents=intents)

# Функция для отображения времени
def format_time(delta):
    return str(delta).split(".")[0]  # убираем миллисекунды

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_member_update(before, after):
    if before.activity != after.activity:  # Если активность изменилась
        if after.activity is not None:
            if isinstance(after.activity, Spotify):
                activity_type = "Spotify"
            elif isinstance(after.activity, Game):
                activity_type = "Game"
            else:
                activity_type = "Other"

            user = after
            activity_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')

            if after.activity.start:  # Если есть время начала
                start_time = after.activity.start.strftime('%Y-%m-%d %H:%M:%S')
                # Запоминаем время начала активности
                activity_start_time[user.id] = start_time

            # Отправляем сообщение с активностью
            message = f"@{user.name} начал {activity_type}: {after.activity.name} в {activity_time}"
            print(message)  # Печать в консоль

            channel = discord.utils.get(user.guild.text_channels, name="общий")  # Можно указать канал, куда отправлять
            if channel:
                await channel.send(message)

        else:  # Когда пользователь перестает играть или использовать активность
            user = after
            if user.id in activity_start_time:
                start_time = activity_start_time[user.id]
                end_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
                time_delta = datetime.now(pytz.timezone('Europe/Moscow')) - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                total_time = format_time(time_delta)
                # Формируем сообщение для завершенной активности
                message = f"@{user.name} завершил {user.activity.name} ({user.activity.type}) с {start_time} до {end_time}, время игры: {total_time}"
                print(message)  # Печать в консоль

                # Отправляем сообщение в канал
                channel = discord.utils.get(user.guild.text_channels, name="общий")  # Указываем канал для сообщений
                if channel:
                    await channel.send(message)

@bot.command()
async def старт(ctx):
    """Команда для начала отслеживания"""
    await ctx.send(f"Начал следить за пользователем @{ctx.author.name}")

@bot.command()
async def стоп(ctx):
    """Команда для остановки отслеживания"""
    await ctx.send(f"Перестал следить за пользователем @{ctx.author.name}")

# Запуск бота
client.run(os.getenv('DISCORD_TOKEN'))
