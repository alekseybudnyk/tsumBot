from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pyzbar.pyzbar import decode
from PIL import Image
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

@dp.message_handler(content_types=['photo'])
async def photo(message):  
        #await bot.send_message(message.from_user.id, 'Got Images')
        file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
        filename, file_extension = os.path.splitext(file_info.file_path)
        
        src = 'photos/'+str(message.from_user.id) +'_'+filename + file_extension 
        await bot.download_file(file_info.file_path,src)
        
        image = Image.open(src)
        decoded = decode(image)
        
        if len(decoded) > 0:
            print(decoded[0].data.decode('utf-8'))
            await bot.send_message(message.from_user.id,'ШК:'+decoded[0].data.decode('utf-8'))
            barcode = decoded[0].data.decode('utf-8')
            response = requests.get('https://api1.tsum.ua:1443/tsum/hs/tsumAPIMobile/thProduct/'+barcode,
            auth = HTTPBasicAuth('it_test', '123456'))
            print('https://api1.tsum.ua:1443/tsum/hs/tsumAPIMobile/thProduct/'+barcode)
            messageText = 'Такий товар не знайдено'

            if response.status_code == 200:

                data = response.json()        
                messageText =  data['Products'][0]['Sku'] + '\n' 
                messageText =  messageText + 'Бренд:   '+data['Products'][0]['Art'] + '\n'
                messageText =  messageText + 'Арт:     '+data['Products'][0]['Brand'] + '\n'
                messageText =  messageText + 'Сезон:   '+data['Products'][0]['Season'] + '\n'
                messageText =  messageText + 'Ціна : '
                
                if data['Products'][0]['Price1'] != '0':
                    messageText =  messageText + '<strike>' + data['Products'][0]['Price1'] + '</strike>'
                messageText =  messageText + ' ' + data['Products'][0]['Price'] 
                
                #if data['Products'][0]['LastUnit'] == '1':
                #    messageText =  messageText + ' <b>Останній розмір</b>'

                await bot.send_message(message.from_user.id,messageText,parse_mode = "HTML")
                
                
                for cr in data['Products'][0]['Colors']:

                    messageText = ''
                    messageText =  messageText + 'Колір:    <b>' + cr['Color'] + '</b>\n' 

                    for sz in cr['Sizes']:
                        if sz['QtyOfSize'] !='0':
                            messageText =  messageText + '<b>'+sz['Size'] + '</b>:'+ '\n'

                        for rm in sz['Rooms']:
                            if rm['Qty'] !='':
                                messageText =  messageText + '  '+rm['Qty'] + ' шт-' + rm['Room']+ '\n'

                    await bot.send_message(message.from_user.id,messageText,parse_mode = "HTML")        
            else:
                await bot.send_message(message.from_user.id,messageText+' '+str(response.status_code),parse_mode = "HTML")
                
        else:
            await bot.send_message(message.from_user.id,'no barcode detected')
 

#============================================================================
@dp.message_handler()
async def echo_send(message : types.Message):
  #  await message.answer(message.text)
  #  await message.reply(message.text)
    await bot.send_message(message.from_user.id, message.text)

executor.start_polling(dp,skip_updates=True)