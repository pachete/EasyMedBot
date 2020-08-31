import os
import sys

from easy_med_bot import message_text_config

from easy_med_bot import config

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
                                  message_text_config.msg_start,
                                  reply_markup = markup
                                 )

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def help(self):
        try:
            text_message = message_text_config.msg_ask_help

            self.bot.send_message(self.chat_id, text_message)

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)
