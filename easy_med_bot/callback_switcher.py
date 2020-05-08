import os
import sys

from easy_med_bot import config

from telebot import types
from random import randint
from easy_med_bot.switcher_class import Switcher
from easy_med_bot.task_handler import randomize_answers


class CallbackSwitcher(Switcher):
    def __init__(self, bot):
        super().__init__(bot)

        self.callback = None
        self.callback_id = None
        self.callback_text = None
        self.split_callback_text = None

        self.message_id = None

    def get_attribute(self):
        return getattr(self, self.split_callback_text[0], lambda: False)

    def process(self, callback):
        try:

            self.callback = callback

            self.chat_id = callback.message.chat.id
            self.callback_id = callback.id
            self.callback_text = callback.data
            self.split_callback_text = self.callback_text.rsplit("_", 1)

            self.message_id = callback.message.message_id
            self.message_text = callback.message.text

            self.bot.answer_callback_query(self.callback_id)
            self.user = config.user_dict[self.chat_id]

            process_command = self.get_attribute()
            process_command()

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def select_step(self):
        try:
            config.user_dict[self.chat_id].step = self.split_callback_text[1]
            if config.user_dict[self.chat_id].step in config.steps:
                self.select_year()

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def select_year(self):
        try:
            self.user.year = self.split_callback_text[1]
            self.user.current_years = config.years[int(self.user.step[-1]) - 1]

            if self.user.year in self.user.current_years:
                self.select_task()
                return

            if self.user.year == "random":
                random_year = randint(0, len(self.user.current_years) - 1)
                self.user.year = self.user.current_years[random_year]
                self.select_random_task()
                return

            else:
                self.generate_year_keyboard()
                return

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def select_task(self):
        try:
            if self.user.task_id > 200:
                return

            self.bot.edit_message_text(
                                       chat_id = self.chat_id,
                                       message_id = self.message_id,
                                       text = self.message_text + "\n",
                                       reply_markup = None
                                      )

            self.generate_task_keyboard()
            self.user.task_id += 1

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def select_random_task(self):
        try:
            self.user.step_type = "random"
            random_id = randint(1, 200)
            self.user.task_id = random_id

            self.bot.edit_message_text(
                                       chat_id = self.chat_id,
                                       message_id = self.message_id,
                                       text = self.message_text + "\n",
                                       reply_markup = None
                                      )

            self.generate_task_keyboard()

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def generate_year_keyboard(self):
        try:
            row_width = len(self.user.current_years)

            markup = types.InlineKeyboardMarkup(row_width = row_width)

            first_row = []
            for year in self.user.current_years:
                first_row.append(types.InlineKeyboardButton(year, callback_data = "select_year_" + year).to_dic())

            markup.keyboard.append(first_row)
            markup.add(types.InlineKeyboardButton("Випадковий тест 🎲", callback_data = "select_year_random"))

            self.user.task_id = 1
            self.bot.edit_message_text(
                                       chat_id = self.chat_id, message_id = self.message_id,
                                       text = "📆 КРОК якого року вас цікавить?" + "\n", reply_markup = markup
                                      )

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def generate_task_keyboard(self):
        try:
            if self.user.step_type == "random":
                length = len(self.user.current_years) - 1
                self.user.year = self.user.current_years[randint(0, length)]
                self.user.task_id = randint(1, 200)

            task = config.tasks_dict[self.user.step + "_" + self.user.year][self.user.task_id]
            task_text, correct_answer = randomize_answers(task)

            if self.user.step_type == "random":
                task_text = self.user.year + " рік\n" + task_text

            print(
                  self.user.task_id, correct_answer,
                  str(self.user.count_correct_answers) + " /", self.user.count_answers
                 )

            if self.user.count_answers != 0 and self.user.count_correct_answers != 0:
                percentage = str((self.user.count_correct_answers * 100) / self.user.count_answers)[:5]
                if percentage[2:] == ".0":
                    percentage = percentage[:2]
                task_text = "*Правильних " + percentage + "%*\n" + task_text

            markup = types.InlineKeyboardMarkup()

            markup.row(
                       types.InlineKeyboardButton("(a) ", callback_data = "answer_a" + correct_answer),
                       types.InlineKeyboardButton("(b) ", callback_data = "answer_b" + correct_answer),
                       types.InlineKeyboardButton("(c) ", callback_data = "answer_c" + correct_answer),
                       types.InlineKeyboardButton("(d) ", callback_data = "answer_d" + correct_answer),
                       types.InlineKeyboardButton("(e) ", callback_data = "answer_e" + correct_answer)
                      )

            self.bot.edit_message_text(
                                       chat_id = self.chat_id,
                                       message_id = self.message_id,
                                       text = task_text,
                                       parse_mode = "Markdown",
                                       reply_markup = markup
                                      )

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def answer(self):
        try:
            user_answer = self.split_callback_text[1][0]
            correct_answer = self.split_callback_text[1][1]

            print(self.user.task_id, user_answer, correct_answer)

            self.user.count_answers += 1

            if user_answer == correct_answer:
                self.user.count_correct_answers += 1
                answer_check = "✅ Правильна відповідь!"
            else:
                answer_check = "⛔ Неправильна відповідь!"

            self.user.current_answer_message = answer_check
            self.bot.edit_message_text(
                                       chat_id = self.chat_id,
                                       message_id = self.message_id,
                                       text = self.message_text.replace('(' + correct_answer + ')', '✅ '),
                                       reply_markup = None
                                      )

            self.generate_answer_keyboard()

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def generate_answer_keyboard(self):
        try:

            markup = types.InlineKeyboardMarkup()

            markup.row(
                       types.InlineKeyboardButton("Наступний тест", callback_data = "select_task_"),
                       types.InlineKeyboardButton("Завершити", callback_data = "end_test_")
                      )

            self.bot.send_message(
                                  chat_id = self.chat_id,
                                  text = self.user.current_answer_message,
                                  reply_markup = markup
                                 )

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)

    def end_test(self):
        try:
            if self.user.step_type != "random":
                msg = "Ви завершили тест КРОК-" + self.user.step[-1] + " " + self.user.year
            else:
                msg = "Ви завершили випадкові тести."

            self.bot.delete_message(
                                    chat_id = self.chat_id,
                                    message_id = self.message_id,
                                    # reply_markup = self.reply_keyboard()
                                   )
            self.bot.send_message(
                                  chat_id = self.chat_id,
                                  text = msg,
                                  reply_markup = self.reply_keyboard()
                                 )
            self.user.step_type = None

        except Exception as current_exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, file_name, exc_tb.tb_lineno)
            print(current_exception)
