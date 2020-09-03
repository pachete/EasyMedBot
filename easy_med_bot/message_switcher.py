import os
import sys

from datetime import datetime
from easy_med_bot import message_text_config
from easy_med_bot.bot import easy_med_bot

from easy_med_bot.task_handler import randomize_answers

from easy_med_bot import config
from easy_med_bot.switcher_class import Switcher
from easy_med_bot.user import User


def search(message):
    try:

        message_text = message.text
        split_search_text = message_text.lower().split()

        if len(split_search_text) < 3:
            msg = easy_med_bot.send_message(
                                            chat_id = message.chat.id,
                                            text = message_text_config.msg_search_error
                                           )
            easy_med_bot.register_next_step_handler(msg, search)
            return

        true_tasks = {}

        for step in config.steps:
            for year in config.years[int(step[-1]) - 1]:
                if step == "STEP3":
                    continue
                current_year_task = config.tasks_dict[step + "_" + year]
                for question in current_year_task[1:]:
                    true_count = 0
                    for split_text in split_search_text:
                        if split_text in question["full_task_text"]:
                            true_count += 1
                            if true_count == len(split_search_text):
                                true_tasks[step + "_" + year + "_" + question["question"].partition(".")[0]] = question

        if len(true_tasks) != 0:
            my_counter = 0
            for key in true_tasks.keys():
                my_counter += 1
                if my_counter == 10:
                    break
                task_text, correct_answer = randomize_answers(true_tasks[key])
                easy_med_bot.send_message(
                        chat_id = message.chat.id,
                        text = task_text + "\n" + "Правильна відповідь: " + correct_answer
                        )

        easy_med_bot.send_message(
                                  chat_id = message.chat.id,
                                  text = "Ви завершили пошук. Кількість результатів: " + str(len(true_tasks)),
                                  reply_markup = config.reply_keyboard_markup()
                                 )

    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)


class MessageSwitcher(Switcher):
    def __init__(self, bot):
        super().__init__(bot)
        self.switcher = {
                         message_text_config.msg_step: self.message_step,
                         message_text_config.msg_search_tests: self.message_search_tests,
                         # "Налаштування⚙": self.message_settings,
                         message_text_config.msg_support_project: self.support
                        }

    def get_attribute(self):
        try:
            if self.chat_id not in config.user_dict.keys():
                date_time_now = datetime.now()
                print("[{}] ".format(date_time_now.strftime("%d/%m/%Y %H:%M:%S")), "first time: ", self.chat_id)
                config.user_dict[self.chat_id] = User(self.chat_id)

            return self.switcher.get(self.message_text)

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def message_step(self):
        try:
            self.generate_step_keyboard()

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def message_search_tests(self):
        try:
            my_msg = message_text_config.msg_start_search

            config.reply_keyboard_markup = self.reply_keyboard

            msg = self.bot.send_message(chat_id = self.chat_id, text = my_msg)
            self.bot.register_next_step_handler(msg, search)

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def message_settings(self):
        pass

    def support(self):

        self.bot.send_message(
                              chat_id = self.chat_id,
                              text = message_text_config.msg_support_me,
                              reply_markup = self.reply_keyboard()
                             )
