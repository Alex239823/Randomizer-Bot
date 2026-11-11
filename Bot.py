import os
import discord
from discord.ext import commands
import random

# Настройка интентов
intents = discord.Intents.default()
intents.message_content = True

# Создаем бота
bot = commands.Bot(command_prefix=['!', '$'], help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f'Бот зашёл как {bot.user}')
    print('Генератор чисел готов к работе!')

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(title='📖 Список команд', description='Вот что я умею:', color=discord.Color.purple())
    embed.add_field(name='`$rand [мин] [макс]`', value='Генерирует случайное число (по умолчанию от 1 до 100)', inline=False)
    embed.add_field(name='`$dice [стороны]`', value='Бросок кубика (по умолчанию d6)', inline=False)
    embed.add_field(name='`$coin`', value='Подбрасывает монетку (Орел/Решка)', inline=False)
    await ctx.send(embed=embed)

@bot.command(name='rand')
async def rand(ctx, min_num: int = 1, max_num: int = 100):
    if min_num > max_num:
        await ctx.send('Минимум не может быть больше максимума!')
        return
    number = random.randint(min_num, max_num)
    await ctx.send(f'🎲 Выпало число: **{number}** (диапазон {min_num}–{max_num})')

@bot.command(name='dice')
async def dice(ctx, sides: int = 6):
    if sides < 2:
        await ctx.send('У кубика должно быть хотя бы 2 стороны!')
        return
    number = random.randint(1, sides)
    await ctx.send(f'🎲 Кубик d{sides}: **{number}**')

@bot.command(name='coin')
async def coin(ctx):
    result = random.choice(['Орёл 🦅', 'Решка 🪙'])
    await ctx.send(f'Подбрасываем... Выпало: **{result}**')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Нужны числа! Пример: `$rand 1 100`')
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        await ctx.send(f'Ошибка: `{error}`')

# Запуск (токен берется из настроек сервера)
bot.run(os.getenv('DISCORD_TOKEN'))
