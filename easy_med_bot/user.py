# import os
# import sys

# from easy_med_bot import config


class User:
    def __init__(self, chat_id):
        self.is_registered = False

        self.chat_id = chat_id

        self.name = None
        self.age = None
        self.gender = None

        self.subject = None
        self.step = None
        self.step_type = None
        self.period = None
        self.year = None
        self.current_years = None

        self.task_id = None
        self.task_text = None
        self.current_answer_message = None

        self.count_answers = 0
        self.count_correct_answers = 0
