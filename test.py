import unittest
from unittest.mock import patch, MagicMock
import os
import telebot
from dotenv import load_dotenv
from Bot import bot, get_dollar_rate
from Bot import check_connection, handle_text


# Загрузка переменных окружения
load_dotenv()


class TestBot(unittest.TestCase):

    def setUp(self):
        # Создаем экземпляр TeleBot с фиктивным токеном
        self.bot = telebot.TeleBot("test_token")

    def test_get_dollar_rate(self):
        # Запрос к API
        with patch('requests.get') as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {'rates': {'RUB': 75.5}}
            mock_request.return_value = mock_response

            # Вызываем тестируемую функцию
            rate = get_dollar_rate()

            # Проверяем результат
            self.assertEqual(rate, 75.5)

    def test_check_connection(self):
        # Создаем фиктивное сообщение
        message = MagicMock()
        message.chat.id = "test_chat_id"

        # Мокаем метод send_message
        with patch.object(self.bot, 'send_message') as mock_send_message:
            check_connection(message)

            # Проверяем, что метод был вызван с правильными аргументами
            mock_send_message.assert_called_once_with(message.chat.id, "Добрый день. Как вас зовут?")

    def test_handle_text(self):
        # Создаем фиктивное сообщение
        message = MagicMock()
        message.text = "иван"
        message.chat.id = "test_chat_id"

        # Мокаем метод send_message и функцию get_dollar_rate
        with patch.object(self.bot, 'send_message') as mock_send_message:
            with patch('Bot.get_dollar_rate') as mock_get_dollar_rate:
                mock_get_dollar_rate.return_value = 76.0

                handle_text(message)

                # Проверяем, что метод был вызван с правильными аргументами
                mock_send_message.assert_called_once_with(message.chat.id,
                                                          "Рад знакомству, Иван! Курс доллара сегодня 76.0р")


if __name__ == '__main__':
    unittest.main()
