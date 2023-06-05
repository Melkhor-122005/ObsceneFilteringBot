import discord
from discord.ext import commands
import asyncio

TOKEN = 'MTA1NzIwMTUwNjQ0MjU1MTM0Ng.GaqTPZ.uT54iCgp22KNovQ6zNWs8PCCe0NvpinedYJuKU'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents = intents)
banned = open('BannedWords2.txt', 'r', encoding='utf-8')
bans = str(banned.read()).split()
#print(bans)
muting = False

#Embed
title = '🔰Info🔰'
description = 'Информация про бота OFBot'
color = 255127
embed = discord.Embed(title=title, description=description, color=color)
embed.add_field(name='📌Данный бот - ваш персональный помощник, если хотите помочь серверу избавиться от грубости и нехороших слов! Вот несколько возможностей бота:', value='◈ Удаление сообщений, содержащих ненормативную лексику \n◈ Предупреждение участников, решивших нарушить покой сообщества \n◈Мут нарушителей, написавших слишком много плохих слов (**если точнее - три**) \nОчистите ваш сервер от грубости!', inline=False)
embed.add_field(name='📋Список команд Бота:', value = '◈ **!OFBot mute** - включает функцию мута пользователей, написавших много запрещённых слов. После трёх предупреждений игрок получает роль *OFB|MUTE*. Используйте ⚙️*Настройки*, чтобы установить разрешения роли! \n◈ **!OFBot unmute** - Отключает систему Предупреждений пользователя (Режим по умолчанию).', inline=False)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready.')

@bot.event
async def on_message(message):
        global muting

        guild = bot.get_guild(message.guild.id)
        member = message.author

    #Message deleting
        for word in message.content.split():
            for i in bans:
                #print(word)
                if i in word.lower() and not message.author.bot:
                    await message.delete()
                    await message.channel.send(f'🔴{message.author.mention} Нарушил правила сервера и сказал плохое слово!🔴')
                    if muting:
                        Warn_1 = discord.utils.find(lambda r: r.name == 'OFB|Warning I', message.guild.roles)
                        Warn_2 = discord.utils.find(lambda r: r.name == 'OFB|Warning II', message.guild.roles)
                        Warn_3 = discord.utils.find(lambda r: r.name == 'OFB|Warning III', message.guild.roles)
                        Mute = discord.utils.find(lambda r: r.name == 'OFB|MUTE', message.guild.roles)

                        if Warn_1 not in member.roles and Warn_2 not in member.roles and Warn_3 not in member.roles and Mute not in member.roles:
                            await message.channel.send("Вам выдано предупреждение **I уровня**!")
                            await member.add_roles(Warn_1)
                        else:
                            if Warn_2 not in member.roles and Warn_3 not in member.roles and Mute not in member.roles:
                                await message.channel.send("Вам выдано предупреждение **II уровня**!")
                                await member.add_roles(Warn_2)
                            else:
                                if Warn_3 not in member.roles and Mute not in member.roles:
                                    await message.channel.send("Вам выдано предупреждение **III уровня**!")
                                    await member.add_roles(Warn_3)
                                else:
                                    if Mute not in member.roles:
                                        await message.channel.send("Вы слишком плохо себя вели! Вам выдаётся мут на **1 час**!")
                                        await member.add_roles(Mute)
                                        await member.remove_roles(Warn_1, Warn_2, Warn_3)
                                        await asyncio.sleep(3600)
                                        await member.remove_roles(Mute)

    #Mute function
        if message.content.startswith('!OFBot mute'):
            if member.guild_permissions.administrator == True:
                if discord.utils.get(member.guild.roles, name="OFB|Warning I") == None:
                    await guild.create_role(name="OFB|Warning I")
                    await guild.create_role(name="OFB|Warning II")
                    await guild.create_role(name="OFB|Warning III")
                    perms = discord.Permissions(send_messages=False, speak=False)
                    await guild.create_role(name="OFB|MUTE", permissions=perms)
                    await message.reply('Бот создал роли-Предупреждения, которые будут получать нарушители! Если данные меры вы считаете излишними, просто напишите: **!OFBot unmute**')
                    muting = True
                    print(muting)
                else:
                    muting = True
                    print('Role Bot wants to create already exists!')
                    await message.reply('Бот *ранее уже создал* роли-Предупреждения, которые будут получать нарушители! Если данные меры вы считаете излишними, просто напишите: **!OFBot unmute**')
                    print(muting)
            else:
                await message.reply('Только администраторам такое под силу!')

    #Unmute function
        if message.content.startswith('!OFBot unmute'):
            if member.guild_permissions.administrator == True:
                if discord.utils.get(member.guild.roles, name="OFB|Warning I") != None:
                    muting = False
                    await message.reply('Теперь нарушители правил сервера перестанут получать роли-Предупреждения! Если вы захотите их вернуть, просто напишите: **!OFBot mute**')
                    print(muting)
                    Warn_1 = discord.utils.find(lambda r: r.name == 'OFB|Warning I', message.guild.roles)
                    Warn_2 = discord.utils.find(lambda r: r.name == 'OFB|Warning II', message.guild.roles)
                    Warn_3 = discord.utils.find(lambda r: r.name == 'OFB|Warning III', message.guild.roles)
                    Mute = discord.utils.find(lambda r: r.name == 'OFB|MUTE', message.guild.roles)
                    for member in guild.members:
                        if Warn_1 in member.roles or Warn_2 in member.roles or Warn_3 in member.roles or Mute in member.roles:
                            await member.remove_roles(Warn_1, Warn_2, Warn_3, Mute)
                else:
                    muting = False
                    print('Warning roles have already been disabled')
                    await message.reply('Команда не сработала! Нельзя отключить роли, которых нет! Если хотите использовать роли-Предупреждения, напишите: **!OFBot mute**')
                    print(muting)
            else:
                await message.reply('Только администраторам такое под силу!')

    #Help
        if message.content.startswith('!OFBot help'):
            await message.reply(embed = embed)
bot.run(TOKEN)
