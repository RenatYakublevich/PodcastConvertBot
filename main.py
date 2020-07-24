import logging

#aiogram и всё утилиты для коректной работы с Telegram API
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pytube import YouTube
from pytube import helpers

import config #конфиг с настройками и API ключями
import youtube_download as yt


#задаём логи
logging.basicConfig(filename="log.log", level=logging.INFO)

#инициализируем бота
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())

@dp.message_handler(commands=['start'],state='*')
async def start(message):
    ''' Функция которая обрабатывает команду /start '''
    await message.answer('Привет я Podcast Converter Bot!🤖\n\nИ я умею конвертировать видео-ролики с ютуба в удобные mp3 подкасты\nПросто отправь мне ссылку и всё!')

@dp.message_handler(lambda message : message.text.startswith('https://') or message.text.startswith('www'))
async def conver_to_podcast(message):
    ''' Функция которая конвертирует видео ролик из ютуба по ссылке в mp3 подксат  '''
    try:

        await message.answer('Подождите немного')
        name_audio_file = 'Для тебя - ' + message.from_user.username

        yt.download_from_youtube(message.text,name_audio_file)

        yt.convert_mp4_to_mp3(name_audio_file)
        with open(f'videos/{name_audio_file}.mp3', 'rb') as podcast:
            await message.answer_audio(audio=podcast,caption='Вот держи свой подкаст!')
        yt.delete_audiofile(name_audio_file)
    except Exception as e:
        await message.answer('Ваша ссылка некоректна!')
        log.exception("Error - " + e)

@dp.message_handler(commands=['about'])
async def except_answer(message : types.Message):
	''' Функция для вывода информации о боте '''
	await message.answer('PodcastConverter version 1.0\nGithub - ')



@dp.message_handler()
async def except_answer(message : types.Message):
	''' Функция непредсказумогого ответа '''
	await message.answer('Я не знаю, что с этим делать 😲\nЯ просто напомню, что есть команда /help')

executor.start_polling(dp, skip_updates=True)
