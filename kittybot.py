from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup
import requests
import logging
import os
from dotenv import load_dotenv


load_dotenv()
secret_token = os.getenv('TOKEN')
secret_URL_cat = os.getenv('URL_cat')
secret_URL_dog = os.getenv('URL_dog')

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

def get_new_image():
    try:
        response = requests.get(secret_URL_cat)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(secret_URL_dog)

    response = response.json()
    random_cat_dog = response[0].get('url')
    return random_cat_dog

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашел'.format(name),
            reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())

def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

    updater.start_polling(poll_interval=20.0)
    updater.idle()

if __name__ == '__main__':
    main()
