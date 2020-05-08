import os
import sys

from easy_med_bot.bot import easy_med_bot
from easy_med_bot import config

from easy_med_bot.command_switcher import CommandSwitcher
from easy_med_bot.callback_switcher import CallbackSwitcher
from easy_med_bot.message_switcher import MessageSwitcher

from easy_med_bot.task_handler import generate_tasks_dict


@easy_med_bot.callback_query_handler(func = lambda call: True)
def handle_callbacks(callback):
    try:
        callback_switcher = CallbackSwitcher(easy_med_bot)
        callback_switcher.process(callback)
    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)


@easy_med_bot.message_handler(commands = config.commands)
def handle_commands(command):
    try:
        command_switcher = CommandSwitcher(easy_med_bot)
        command_switcher.process(command)
    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)


@easy_med_bot.message_handler(content_types = ["text"])
def handle_messages(message):
    try:
        message_switcher = MessageSwitcher(easy_med_bot)
        message_switcher.generate_step_keyboard()
        message_switcher.process(message)
    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)


def main():
    try:
        easy_med_bot.enable_save_next_step_handlers(delay = 2)
        easy_med_bot.load_next_step_handlers()
        easy_med_bot.polling(none_stop = True)
    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)


if __name__ == '__main__':
    try:
        config.tasks_dict = generate_tasks_dict()
        print("Bot is loaded")
        main()
    except Exception as main_exception:
        print(main_exception)
