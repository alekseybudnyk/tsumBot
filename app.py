from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os
import requests
from requests.auth import HTTPBasicAuth

bot = Bot(token='5807710356:AAENK0tO3zvdzqgK54vHhRrOineIYr8oX2o')
dp = Dispatcher(bot)



#============================================================================
@dp.message_handler(commands=['start','help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привіт')
        await message.delete()
    except:
        await message.reply('Спілкування з ботом в особистих повідомленнях')    

executor.start_polling(dp,skip_updates=True)