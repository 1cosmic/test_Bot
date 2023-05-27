import random

from aiogram import  types

button_text = {
    "go_to_game": "Начинаем! ▶️",

    "name_yes": "Да!",
    "name_no": "Нет, повторить",

    "reg_yes": "Да",
    "reg_no": "Нет",

    "skip_quest": "Пропустить 🆘"
}
# Комплект кнопок для ответа пользователя
buttons_of_regs = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    types.KeyboardButton(text=button_text["reg_yes"]),
    types.KeyboardButton(text=button_text["reg_no"])
)

# Кнопка старта регистрации.
button_of_start = types.InlineKeyboardMarkup(resize_keyboard=True)
button_of_start.add(
    types.InlineKeyboardButton(text=button_text["go_to_game"], callback_data="!reg"))

# Клавиатура старта регистрации.
key_of_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_of_start.add(
    types.KeyboardButton(text=button_text["go_to_game"], callback_data="!reg"))


# Кнопка запуска игры.
button_of_run = types.InlineKeyboardMarkup(resize_keyboard=True)
button_of_run.add(
    types.InlineKeyboardButton(text=button_text["go_to_game"], callback_data="!run"))

# Клавиатура старта регистрации.
key_of_run = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_of_run.add(
    types.KeyboardButton(text=button_text["go_to_game"], callback_data="!run"))


button_of_skip = types.InlineKeyboardMarkup(resize_keyboard=True)
button_of_skip.add(types.KeyboardButton(text=button_text["skip_quest"], callback_data="!skip_quest"))


# Словарь всех кнопок.
Buttons = {
    "b_start": button_of_start,

    "b_regs": buttons_of_regs,
    "k_start": key_of_start,

    "b_run": button_of_run,
    "k_run": key_of_run,

    "skip_quest": button_of_skip,
}


# Кнопки ответов.

class Answers_buttons():

    def __init__(self, list_answers):
        self.keyboard = None
        self.buttons = [
            types.KeyboardButton(list_answers[0]),
            types.KeyboardButton(list_answers[1]),
            types.KeyboardButton(list_answers[2]),
            types.KeyboardButton(list_answers[3]),
        ]

        # for answer in list_answers:
        #     self.buttons.append(types.KeyboardButton(answer))

        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).row(self.buttons[0],
                                                                                         self.buttons[1],
                                                                                         self.buttons[2],
                                                                                         self.buttons[3])

    def restruct(self):
        # self.__answers = list_answers

        random.shuffle(self.buttons)

        return self.keyboard



answ = ["1", "2", "3", "4"]

Buttons_answers = {
    1: Answers_buttons(["3", "2", "5", "8"]),
    2: Answers_buttons(["1675", "18823", "2341", "1759"]),
    3: Answers_buttons(["Тигр", "Медведь", "Обезьяна", "Лиса"]),
    4: Answers_buttons(["Лестница", "Самолет", " Цветок", "Бабочка"]),
    5: Answers_buttons(["Траграм", "Танграм", "Тарам-тарам", "Тортграм"]),
    6: Answers_buttons(answ),
    7: Answers_buttons(answ),
    8: Answers_buttons(answ),
}