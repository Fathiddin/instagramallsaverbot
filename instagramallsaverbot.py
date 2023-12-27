import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor
from aiogram import types
from aiogram.dispatcher.filters import Text


import requests
import json

def instadownloader(link):
    url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"

    querystring = {"url":link}

    headers = {
        "X-RapidAPI-Key": "9dee38a6bemshe34bd0a258feb27p1629b1jsnabd9485ff439",
        "X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    rest = json.loads(response.text)
    if 'error' in rest:
        return 'Bad'
    else:
        dict = {}
        if rest['Type'] =='Post-Image':
            dict['type'] ='image'
            dict['media']=rest['media']
            return dict
        elif rest['Type'] =='Post-Video':
            dict['type'] ='video'
            dict['media']=rest['media']
            return dict
        elif rest['Type'] =='Carousel':
            dict['type'] ='carousel'
            dict['media']=rest['media']
            return dict
        else:
            return 'Bad'
        return dict

BOT_TOKEN = "6948532136:AAFLWQL_KJ8M7SeaS6f7zY9V3-Vuiw6IcSc"
CHANNEL_ID = "-1002100002580"




logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    channel = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
    
    if channel['status']!='left':
        await message.answer("Botdan foydalanishiz mumkin! Videomanzilni yuboring")
        @dp.message_handler(Text(startswith='https://www.instagram.com/'))
        async def insta(message:types.Message):
            link = message.text
            data = instadownloader(link=link)
            if data == 'Bad':
                await message.answer("Bu manzil orqali hech narsa topilmadi")
            else:
                if data['type']=='image':
                    await message.answer_photo(photo=data['media'])
                elif data['type']=='video':
                    await message.answer_video(video=data['media'])
                elif data['type']=='carousel':
                        for i in data['media']:
                            await message.answer_document(document=i)
                else:
                    await message.answer("Bu manzil orqali hech narsa topilmadi")
    else:
        inline=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Kanalga obuna bo'lish", url="https://t.me/davies_blog")],
                [InlineKeyboardButton(text="Obuna bo'lish", callback_data="azo")]
            ],
            row_width=2
        )
        await message.answer("Botdan foydalanish uchun quyidagi kanalga obuna bo'ling", reply_markup=inline)
        
@dp.callback_query_handler(lambda c: c.data=="azo")
async def callback(callback:types.CallbackQuery):
    channel = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback.from_user.id)
    
    if channel['status']!='left':
        await callback.message.answer("Botdan foydalanishiz mumkin!")
    else:
        inline=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Kanalga obuna bo'lish", url="https://t.me/davies_blog")],
                [InlineKeyboardButton(text="Obuna bo'lish", callback_data="azo")]
            ],
            row_width=2
        )
        await callback.message.answer("Obuna bolmadingiz kanalga obuna bo'ling", reply_markup=inline)
        
if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)