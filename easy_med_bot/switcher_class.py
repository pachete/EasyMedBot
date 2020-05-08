import os
import sys

from easy_med_bot import config

from telebot import types
from easy_med_bot import config


class Switcher:
    def __init__(self, bot):
        self.bot = bot
        self.user = None

        self.all_tasks = config.tasks_dict

        self.message = None
        self.message_text = None

        self.chat_id = None

    def get_attribute(self):
        return getattr(self, self.message_text, lambda: False)

    def process(self, message):
        try:
            self.message = message
            self.message_text = message.text

            self.chat_id = message.chat.id

            process_command = self.get_attribute()
            process_command()
        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def reply_keyboard(self):
        try:
            markup = types.ReplyKeyboardMarkup(True, True)
            markup.row(
                       types.InlineKeyboardButton("КРОК📝", callback_data = "select_step_"),
                       types.InlineKeyboardButton("Пошук по тестам🔎️", callback_data = "search_book_")
                      )
            markup.row(
                       # types.InlineKeyboardButton("Налаштування⚙", callback_data = ""),
                       types.InlineKeyboardButton("Підтримати проект💰💪", callback_data = "")
                      )
            return markup
        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def generate_step_keyboard(self):
        try:
            if not self.message_text:
                return
            markup = types.InlineKeyboardMarkup()
            markup.row(
                    types.InlineKeyboardButton("КРОК-1", callback_data = "select_step_STEP1"),
                    types.InlineKeyboardButton("КРОК-2", callback_data = "select_step_STEP2"),
                    types.InlineKeyboardButton("КРОК-3", callback_data = "select_step_STEP3")
                    )
            self.bot.send_message(self.chat_id, "🤔Яка база данних КРОК вас цікавить?", reply_markup = markup)
        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)
