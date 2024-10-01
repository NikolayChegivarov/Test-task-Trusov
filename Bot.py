import os
import telebot
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


def get_dollar_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    rate = data['rates']['RUB']
    return round(rate, 2)


@bot.message_handler(commands=['start', 'connect'])
def check_connection(message):
    try:
        bot.send_message(message.chat.id, f"Добрый день. Как вас зовут?")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {str(e)}")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_name = message.text.strip().capitalize()
    dollar_rate = get_dollar_rate()
    bot.send_message(message.chat.id, f"Рад знакомству, {user_name}! Курс доллара сегодня {dollar_rate}р")


bot.polling(none_stop=True)

if __name__ == '__main__':
    bot.polling(none_stop=True)
