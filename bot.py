import discord
import os
import datetime

intents = discord.Intents.default()  # Создание объекта intents
intents.message_content = True  # Разрешение на получение сообщений
client = discord.Client(intents=intents)  # Передача intents при создании клиента

tracking = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_member_update(before, after):
    if before.activity != after.activity:
        if after.activity:
            # Начало отслеживания новой активности
            tracking[after.user.id] = {
                'game': after.activity.name,
                'start': datetime.datetime.now()
            }
            print(f"Started tracking {after.user.name}'s activity: {after.activity.name}")

        elif after.activity is None and after.user.id in tracking:
            # Окончание отслеживания активности
            end_time = datetime.datetime.now()
            time_spent = end_time - tracking[after.user.id]['start']
            start_time = tracking[after.user.id]['start'].strftime('%Y-%m-%d %H:%M:%S')
            end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

            # Отправка сообщения с результатами
            user = client.get_user(after.user.id)
            await user.send(f"@{after.user.name} - {tracking[after.user.id]['game']}/@{start_time} @ {end_time} @ {str(time_spent)}")
            print(f"Stopped tracking {after.user.name}'s activity: {tracking[after.user.id]['game']}")

            del tracking[after.user.id]

client.run('YOUR_BOT_TOKEN')