import os
import sys

from easy_med_bot import config

from telebot import types
from easy_med_bot.switcher_class import Switcher
from easy_med_bot.user import User


class CommandSwitcher(Switcher):
    def __init__(self, bot):
        super().__init__(bot)

    def get_attribute(self):
        try:
            print(self.message_text[1:])
            return getattr(self, self.message_text[1:], lambda: False)

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def start(self):
        try:

            if self.chat_id not in config.user_dict.keys():
                print("ok", self.chat_id)
                config.user_dict[self.chat_id] = User(self.chat_id)

            markup = self.reply_keyboard()

            self.bot.send_message(
                                  self.chat_id,
                                  "Вас вітає EasyMed bot🤖\n" +
                                  "Щоб дізнатись як користуватись ботом - відправте /help",
                                  reply_markup = markup
                                 )

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def help(self):
        try:
            text_message = "Для того, щоб почати роботу - оберіть необхідну опцію на клавіатурі знизу. " \
                           "\nНема клавіатури? Введіть /start і все стане на свої місця🙃\n" \
                           "Хочете пройти тестування КРОК - тисніть на відповідну кнопку, " \
                           "оберіть яку базу хочете (КРОК 1,2 або 3) та рік. Проходьте тести😊" \
                           "Для пошуку тесту - тисніть відповідну кнопку та вводьте пошуковий запит😉\n" \
                           "Сподобався бот? Підтримай проект! " \
                           "Інформація про те як це зробити у розділі \"Підтримати проект💰💪\""

            self.bot.send_message(self.chat_id, text_message)

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)
