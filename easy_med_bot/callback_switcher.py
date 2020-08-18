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

            if self.user.step == "STEP3":
                self.user.period = "AUTUMN"

            if self.user.step != "STEP3":
                self.user.period = ""

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
            for year in self.user.current_years[::-1]:
                first_row.append(types.InlineKeyboardButton(
                                                            year,
                                                            callback_data = "select_year_" + year
                                                           ).to_dic())

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

            period = ""
            task_text = ""

            # print(config.tasks_dict.keys())

            if self.user.period == "AUTUMN":
                period = "AUTUMN-"

            if self.user.step_type == "random":
                length = len(self.user.current_years) - 1
                self.user.year = self.user.current_years[randint(0, length)]
                self.user.task_id = randint(1, len(config.tasks_dict[self.user.step + "_" +
                                                                     period + self.user.year]))
                task_text = self.user.year + " рік\n"

            # if self.user.step == "STEP3":
            #    period += "-"

            task = config.tasks_dict[self.user.step + "_" + period + self.user.year][self.user.task_id]
            task_and_answer = randomize_answers(task)

            task_text += task_and_answer[0]
            correct_answer = task_and_answer[1]

            print(
                  self.user.task_id, correct_answer,
                  str(self.user.count_correct_answers) + " /", self.user.count_answers
                 )

            task_number = len(config.tasks_dict[self.user.step + "_" + period + self.user.year]) - 1
            task_ratio = " {}/{}".format(self.user.count_correct_answers, task_number)

            if self.user.count_answers != 0 and self.user.count_correct_answers != 0:
                percentage = str((self.user.count_correct_answers * 100) / task_number)[:5]
                if percentage[2:] == ".0":
                    percentage = percentage[:2]
            #     task_text = "*Правильних " + percentage + "%*" + task_ratio + "\n" + task_text
            # else:
            #     task_text = "*Правильних 0%* " + task_ratio + "\n" + task_text

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
            # print(self.message_text.partition("\n")[0])
            split_message_text = self.message_text.partition("\n")
            self.message_text = "*" + split_message_text[0] + "*\n" + split_message_text[2]
            self.bot.edit_message_text(
                                       chat_id = self.chat_id,
                                       message_id = self.message_id,
                                       text = self.message_text.replace('(' + correct_answer + ')', '✅ '),
                                       parse_mode = "Markdown",
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

            period = ""
            task_number = len(config.tasks_dict[self.user.step + "_" + period + self.user.year]) - 1

            if self.user.period == "AUTUMN":
                period = "AUTUMN-"

            if self.user.step_type != "random":
                msg = "Ви завершили тест КРОК-" + self.user.step[-1] + " " + self.user.year + "\n"
                msg += "Ви дійшли до завдання номер " + str(self.user.task_id - 1) + "\n"
                msg += "Загальний результат по тесту: "
                msg += str(100 * (self.user.count_correct_answers / task_number)) + "%"
                msg += " (" + str(self.user.count_correct_answers) + "/" + str(task_number) + ")"
            if self.user.step_type == "random":
                msg = "Ви завершили випадкові тести.\n"
                msg += "Результат: ".format(self.user.count_answers)
                msg += str(100 * (self.user.count_correct_answers / self.user.count_answers)) + "%"
                msg += " (" + str(self.user.count_correct_answers) + "/" + str(self.user.count_answers) + ")"

            self.user.count_correct_answers = 0

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
