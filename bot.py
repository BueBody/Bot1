import discord
import datetime

# Настройка intents для отслеживания активности
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True  # Нужно для отслеживания активности

client = discord.Client(intents=intents)

# Словарь для отслеживания времени и игры
tracking = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_member_update(before, after):
    # Проверяем, изменился ли статус активности
    if before.activity != after.activity:
        # Если появилась новая активность
        if after.activity:
            # Записываем время начала
            tracking[after.user.id] = {
                'game': after.activity.name,
                'start': datetime.datetime.now()
            }
            print(f"Started tracking {after.user.name}'s activity: {after.activity.name}")

        elif after.activity is None and after.user.id in tracking:
            # Если активность закончилась, считаем время и отправляем отчет
            end_time = datetime.datetime.now()
            time_spent = end_time - tracking[after.user.id]['start']
            start_time = tracking[after.user.id]['start'].strftime('%Y-%m-%d %H:%M:%S')
            end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

            # Отправляем результат в личные сообщения
            user = client.get_user(after.user.id)
            if user:
                await user.send(f"@{after.user.name} - {tracking[after.user.id]['game']} / @{start_time} @ {end_time} @ {str(time_spent)}")

            print(f"Stopped tracking {after.user.name}'s activity: {tracking[after.user.id]['game']}")
            del tracking[after.user.id]

client.run('YOUR_BOT_TOKEN')
