import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1945582452:AAGvm9x_qM6b7uEiOcwS-JCzUGjyM2Yf_0s'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message, kb=None):
    fam = message.from_user.last_name
    ism = message.from_user.first_name

    await message.reply(
        "Assalomu Alaykum {} {}\n\nShu tartibda jo'nating:\n1:2 audio yoki 1:2 text\nko`rinishida jo`nating!\n\nBu yerda 1 birinchi sura 2 esa shu suradagi oyat\n\n#Eslatma\nAudio: Shayx Mishary Roshid\nTafsir: Shayx Alouddin Mansur".format(
            fam, ism))


@dp.message_handler()
async def send_audio(message: types.Message):
    key = message.text.split(' ')
    nw = key[0].split(':')
    try:
        if key[1] == 'audio':
            url = 'http://api.alquran.cloud/v1/ayah/{}:{}/ar.alafasy'.format(nw[0], nw[1])
            res = requests.get(url)
            r = res.json()
            audio = r['data']['audio']
            await bot.send_audio(chat_id=message.from_user.id, audio=audio)
        elif key[1] == 'text':
            url1 = 'https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-alauddinmansour/{}/{}.json'.format(
                nw[0], nw[1])
            url = 'http://api.alquran.cloud/v1/ayah/{}:{}/ar.alafasy'.format(nw[0], nw[1])
            res = requests.get(url)
            r = res.json()
            res1 = requests.get(url1)
            r1 = res1.json()
            text_arab = r['data']['text']
            text_uzb = r1['text']

            await message.reply(text_arab + '\n\n' + text_uzb)
    except:
        await message.reply(
            'No`to`g`ri formatda jo`natyapsiz!\nIltimos:\n\n1:2 audio yoki 1:2 text\nko`rinishida jo`nating!\n\nBu yerda 1 birinchi sura 2 esa shu suradagi oyat')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
