import os
import sys

from easy_med_bot import config

from docx2txt import process


def replace_characters(text):
    try:
        characters = ["*", "\\"]
        for character in characters:
            text.replace(character, "")
        text.strip()
    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)


def open_year_file(current_step, current_year):
    try:
        '''
        This function opens a file that corresponds to passed step and year.
        step is a dictionary that contains all tasks for selected year and step.
        it's format goes as following:
        step = [
                current_year
                task1
                task2
                task3
                ....
                last_task
               ]
        '''
        step = [current_year]
        file_name = "STEPS/{}/{}.docx".format(current_step, current_year)
        file_name = "easy_med_bot/" + file_name
        file_text = process(file_name)
        split_file_text = file_text.split('\n\n')
        question_id_list = [question_id for question_id in range(0, len(split_file_text), 6)]

        print(len(split_file_text), current_step, current_year)

        for question_id in question_id_list:

            # print(current_year, current_step)
            # print(question_id)

            question = split_file_text[question_id].replace("\\", "")

            full_task_test = " "

            full_task_test.join(
                                [split_file_text[answer_id].lower()
                                for answer_id in range(question_id + 1, question_id + 6)]
                               )

            full_task_test = question.lower() + " " + full_task_test

            answer_set = set([split_file_text[answer_id].replace("*", "").replace("\\", "").strip()
                           for answer_id in range(question_id + 1, question_id + 6)])

            correct_answer = split_file_text[question_id + 1].replace("*", "").strip()

            current_task = {
                            "question": question,
                            "answers": answer_set,
                            "correct_answer": correct_answer,
                            "full_task_text": full_task_test
                           }

            step.append(current_task)

        return step

    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)


def generate_tasks_dict():
    try:

        tasks_dict = dict()

        for step in config.steps:
            for year in config.years[int(step[-1]) - 1]:
                period = ""
                if step == "STEP3" and year == "2019":
                    period = "AUTUMN-"
                tasks_dict[step + "_" + period + year] = open_year_file(step, period[:-1] + "/" + year)

        return tasks_dict

    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)


def randomize_answers(task):
    try:
        answers = ''
        letter_id = 0
        correct_letter = ''

        letters = ["a", "b", "c", "d", "e"]
        letters_in_brackets = ["(a) ", "(b) ", "(c) ", "(d) ", "(e) "]

        for answer in task['answers']:
            if letter_id < 5:
                if answer == task['correct_answer']:
                    correct_letter = letters[letter_id]
                answers += letters_in_brackets[letter_id] + answer + '\n'
                letter_id += 1
        task_text = (task['question'] + '\n' + answers).strip()

        return task_text, correct_letter

    except Exception as current_exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, file_name, exc_tb.tb_lineno)
        print(current_exception)
