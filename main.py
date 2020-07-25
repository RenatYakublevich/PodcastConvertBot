import logging
import telebot
import config #конфиг с настройками и API ключями
import youtube_download as yt


#задаём логи
logging.basicConfig(filename="log.log", level=logging.INFO)

#инициализируем бота
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    ''' Функция которая приветсвует пользователя после команды /start или /help '''
	bot.send_message(message.chat.id, "Привет я Podcast Converter Bot!🤖\n\nИ я умею конвертировать видео-ролики с ютуба в удобные mp3 подкасты\nПросто отправь мне ссылку и всё!")

@bot.message_handler(func=lambda message: message.text.startswith('https://') or message.text.startswith('www'))
def conver_to_podcast(message):
    ''' Функция которая конвертирует видео ролик из ютуба по ссылке в mp3 подксат  '''
    try:

        bot.send_message(message.chat.id,'Подождите немного')
        name_audio_file = 'Для тебя - ' + message.from_user.username

        yt.download_from_youtube(message.text,name_audio_file)

        yt.convert_mp4_to_mp3(name_audio_file)
        with open(f'videos/{name_audio_file}.mp3', 'rb') as podcast:
            bot.send_audio(message.chat.id, podcast)
        yt.delete_audiofile(name_audio_file)
    except Exception as e:
        bot.send_message(message.chat.id,'Ваша ссылка некоректна!')
        log.exception("Error - " + e)

@bot.message_handler(commands=['about'])
def about(message):
	''' Функция для вывода информации о боте '''
	bot.send_message(message.chat.id,'PodcastConverter version 1.0\nGithub - https://github.com/RenatYakublevich/PodcastConvertBot')



@bot.message_handler()
def except_answer(message):
	''' Функция непредсказумогого ответа '''
	bot.send_message(message.chat.id,'Я не знаю, что с этим делать 😲\nЯ просто напомню, что есть команда /help')

bot.polling(none_stop=True)
