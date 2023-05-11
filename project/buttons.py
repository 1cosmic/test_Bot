from aiogram import  types

button_text = {
    "go_to_game": "Начинаем!",

    "name_yes": "Да!",
    "name_no": "Нет, повторить",

    "reg_yes": "Да",
    "reg_no": "Нет",
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




# Словарь всех кнопок.
Buttons = {
    "b_start": button_of_start,

    "b_regs": buttons_of_regs,
    "k_start": key_of_start,

    "b_run": button_of_run,
    "k_run": key_of_run,
}