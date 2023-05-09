import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv('.env')
api_key = os.getenv('API_KEY')
bot_key = os.getenv('BOT_KEY')
bot = telebot.TeleBot(bot_key)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_key, file_info.file_path))
    with open('voice.ogg', 'wb') as f:
        f.write(file.content)
    r = requests.post('https://stt.api.cloud.yandex.net/speech/v1/stt:recognize', headers={'Authorization': 'Api-Key {}'.format(api_key)}, data=file.content, params={'lang': 'ru-RU'})
    if r.status_code == 200:
        text = r.json().get('result')
        if text:
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, 'Не удалось распознать текст.')
    else:
        bot.reply_to(message, 'Произошла ошибка при распознавании аудио.')

bot.polling()
