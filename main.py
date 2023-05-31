import asyncio
from copy import copy
from random import shuffle, randint
import re
from time import time
import datetime

from project import config

from project.users import User
from project.buttons import Buttons, button_text, Buttons_answers
from project.utils import States, States_Quest, code_Morze
from project.video_notes import Video_Notes
from project.skeleton_quest import create_quests
from project.messages import quests_welcomes, quests_answers, quests_dops, quests_hints, welcome_start, reg_start

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from asyncio import sleep

# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# Функции для внутренней работы программы (автоматизаторы).

filter_char_name = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

counter_help = 3
count_user_in_quest = 3
timeout = 3600

time_await = {
    "text": 1,
    "video": 5,
    "video_quest": 3,
}

# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
### ==========

# Для инициализации токена необходимо вбить его вместо config.TOKEN.
# Однако, если вы хотите работать в команде и с git`ом, то лучше заведите файл config,
# в котором создайте переменную TOKEN и присвойте ей значение вашего TG-бота.

token = config.TOKEN
videos = Video_Notes()

# bd = BD()

### ==========

# Создаём асинхронного бота.
tg_bot = Bot(token)
dispatcher = Dispatcher(tg_bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())

# Список пользователей, проходящих регистрацию.
pre_register_user = []

# Заводим список пользователей, зарегистрированных на прохождение.
list_user = {}

# Список пользователей, находящихся в очереди на прохождение (в случае пробок).
await_user = []

# Создаём список квестов для прохождения.
list_quest = create_quests()

# Notify admin:
finished_quest = []
id_admin = 867140367
date_notify = datetime.date.today()


def cleaner():
    """
    Очищает список прошедших пользователей.
    :return:
    """



async def register(msg):

    id = msg.from_user.id
    state = dispatcher.current_state(user=id)
    await state.set_state(States.AWAIT[0])

    id_ = msg.from_user.id
    username = msg.from_user.username

    list_user[id_] = User(id_, username, None, state, len(list_quest))
    pre_register_user.remove(id_)

    await tg_bot.send_video_note(id_, videos.dops["hello_start"], reply_markup=types.ReplyKeyboardRemove())
    await sleep(time_await["video"])

    await tg_bot.send_message(id_, welcome_start["reg"])
    await sleep(time_await["text"])
    await tg_bot.send_message(id_, welcome_start['reg_ask_name'])

    await state.set_state(States.REGISTER[0])


async def welcome_to_the_Quest(user):

    id_quest = user.get_cur_quest().id_

    for video in videos.question[id_quest]:
        await tg_bot.send_video_note(user.id_, video)
        await sleep(time_await["video"])

    await tg_bot.send_message(user.id_, quests_welcomes[id_quest].format(user.name),
                              reply_markup=types.ReplyKeyboardRemove())

    if id_quest in range(1, 9):
        await sleep(time_await["text"])
        await tg_bot.send_message(user.id_, "Выбери правильный ответ.", reply_markup=Buttons_answers[id_quest].restruct())


async def quest_processor(msg, id_quest):

    id_ = msg.from_user.id
    user = list_user[id_]
    # print(f"Попытка пользователя № {user.get_counter_attemps()}")

    if msg.text.lower() in quests_answers[id_quest]:

        videos_true = videos.dops["answer_true"]
        random_video = randint(0, len(videos_true) - 1)

        await tg_bot.send_video_note(id_, videos_true[random_video])
        await sleep(time_await["video_quest"])

        await msg.answer(quests_dops["True"], reply_markup=types.ReplyKeyboardRemove())
        await sleep(time_await["text"])

        return True

    else:
        # Отправляем нужную подсказку в соответствии с числом попыток.
        if user.get_counter_attemps() >= 2:
            user.reset_counter_attemps()

        flag_for_hints = user.get_counter_attemps()

        videos_false = videos.dops["answer_false"]
        random_video = randint(0, len(videos_false) - 1)

        await tg_bot.send_video_note(id_, videos_false[random_video])
        await sleep(time_await["video_quest"])

        await msg.answer(quests_dops["False"])
        await sleep(time_await["text"])

        if id_quest in videos.hint.keys():
            if flag_for_hints < len(videos.hint[id_quest]):

                await tg_bot.send_video_note(id_, videos.hint[id_quest][flag_for_hints])
                await sleep(time_await["video_quest"])

        if id_quest in quests_hints.keys():

            await msg.reply(quests_hints[id_quest][flag_for_hints])
            await sleep(time_await["text"])

        user.up_counter_attemps()

        # # Если квест с 1 по 9 - даём выбор правильных ответов.
        if id_quest in range(1, 9):
            await msg.answer("Выбери правильный ответ.", reply_markup=Buttons_answers[id_quest].restruct())

        # Проверяем, нужна ли ему помощь пропустить квест.
        if user.get_counter_help() >= counter_help:

            await tg_bot.send_message(id_, "Задание слишком сложное? Нажми кнопку \"Пропустить\".",
                                      reply_markup=Buttons["skip_quest"])

        else:
            user.up_counter_help()


async def quest_dispatcher(msg):

    id_ = msg.from_user.id
    user = list_user[id_]
    state = user.state

    # Если у пользователя уже установлен квест (из очереди).
    user_quest = user.get_cur_quest()
    if user_quest != None:

        return False

    # Фильтруем и сортируем квесты.
    quests = sorted(list_quest, key=lambda x: x.getCountUser())
    quests = list(filter(lambda q: q.getCountUser() < count_user_in_quest, quests))
    shuffle(quests)

    if len(quests) > 0:

        for q in quests:
            if q.id_ in user.required_quests():

                q.addUser(user)
                user.set_cur_quest(q)
                return True

    else:
        
        if user.id_ not in await_user:
            await_user.append(id_)

        return False


def quest_quit(user):

    # state = user.state

    quest = user.get_cur_quest()

    if quest != None:
        quest.removeUser(user)

        user.pop_quest(quest.id_)
        user.set_cur_quest(None)
        user.reset_counter_attemps()
        user.reset_counter_help()

        print(f"Пользователь {user.name} вышел из {quest.name}")

        return quest


def await_user_dispatcher(quest):


    for u in copy(await_user):
        user = list_user[u]

        if user.get_cur_quest() == None:
            if quest.id_ in user.required_quests():

                quest.addUser(user)
                user.set_cur_quest(quest)
                await_user.remove(u)

                return user

    return False


# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=

@dispatcher.message_handler(state='*', commands=['start'])
async def start(message: types.Message):
    # TODO: Изменить приветствие, добавить медиа и т.п.

    id = message.from_user.id

    # Добавляем пользователя в очередь на регистрацию.
    if (id not in pre_register_user) and (id not in list_user.keys()):
        pre_register_user.append(id)

        # Приветствие.

        await message.answer(welcome_start['hello'], reply_markup=Buttons['k_start'])
        await sleep(time_await["text"])
        await tg_bot.send_message(id, welcome_start['hello_2'], reply_markup=Buttons['b_start'])

        return True

    if id in list_user.keys():
        await message.answer("Ты уже зарегистрирован. Продолжай прохождение!")



@dispatcher.message_handler(state="*", commands=["restart"])
async def restart_game(msg: types.Message):
    """
    Сбрасывает все состояния пользовател, переводя его в режим регистрации.
    :param msg:
    :return:
    """

    id_ = msg.from_user.id

    if id_ in list_user.keys():
        user = list_user[id_]

        if user.get_cur_quest() != None:

            vacated_quest = quest_quit(user)
            vacated_user = await_user_dispatcher(vacated_quest)

            if vacated_user != False and vacated_quest != None:
                await tg_bot.send_message(vacated_user.id_, quests_dops["await_go"], reply_markup=Buttons["k_run"])

            # await user.state.set_state(States.GO_TO_NEXT[0])
            #
            # await msg.answer(reg_start['start?'], reply_markup=Buttons["b_run"])

    if id_ in pre_register_user:
        pre_register_user.remove(id_)

    if id_ in await_user:
        await_user.remove(id_)

    if id_ in list_user.keys():
        await list_user[id_].state.reset_state()
        list_user.pop(id_)


@dispatcher.message_handler(state=States.GOODBYE)
async def goodbye(msg: types.Message):
    await msg.reply("Ты успешно прошёл все испытания! Скорее подходи к администратору музея, мы ждём тебя ;)")


@dispatcher.message_handler(state=States.AWAIT)
async def wait(msg: types.Message):

    pass
    # await msg.reply("Ожидай.")




@dispatcher.callback_query_handler(lambda x: x.data == "!skip_quest", state=States_Quest.all())
async def skip_game(msg: types.Message):
    """
    Выход из игры.
    """

    user_id = msg.from_user.id
    user = list_user[user_id]
    quest = user.get_cur_quest()

    state = user.state
    await state.set_state(States.AWAIT[0])

    if user.get_counter_help() >= counter_help:

        # Убавляем счётчик личных побед пользователя.
        user.reduce_win()

        if quest.id_ == 0:
            answer = user.morze

        else:
            answer = quests_answers[quest.id_]

        await tg_bot.send_message(user_id,
                                  f"Не печалься! В следующий раз обязательно получится 😉 \nПравильный ответ: {answer[0]}")


        # Блок кода - выход. Пользователь выходит из квеста, который затем отправляется по очереди.
        vacated_quest = quest_quit(user)
        vacated_user = await_user_dispatcher(vacated_quest)

        if vacated_user != False and vacated_quest != None:
            await tg_bot.send_message(vacated_user.id_, quests_dops["await_go"], reply_markup=Buttons["k_run"])


        await user.state.set_state(States.GO_TO_NEXT[0])

        await tg_bot.send_message(user_id, reg_start['start?'], reply_markup=Buttons["b_run"])
        return
        ###

    else:
        await state.set_state(States_Quest.all()[quest.id_])


@dispatcher.message_handler(state=States_Quest.all(), commands=['quit'])
async def quit_from_game_command(msg: types.Message):
    """
    Выход из игры.

    :return:
    """

    await msg.answer("Выходим из задания.")

    id = msg.from_user.id
    user = list_user[id]
    await user.state.set_state(States.AWAIT[0])

    # print(f"Пользователь {user.name} принудительно выходит из игры.")

    # Блок кода - выход. Пользователь выходит из квеста, который затем отправляется по очереди.
    vacated_quest = quest_quit(user)
    vacated_user = await_user_dispatcher(vacated_quest)

    if vacated_user != False and vacated_quest != None:
        await tg_bot.send_message(vacated_user.id_, quests_dops["await_go"], reply_markup=Buttons["k_run"])


    await user.state.set_state(States.GO_TO_NEXT[0])

    await msg.answer(reg_start['start?'], reply_markup=Buttons["b_run"])
    return
    ###



##### =================================
####
##
# Обработка сигналов после регистрации -> старт прохождения квестов.

@dispatcher.message_handler(state=States.GO_TO_NEXT)
async def processed_go_to_next(msg: types.Message):

    id_ = msg.from_user.id
    user = list_user[id_]
    state = user.state

    await state.set_state(States.AWAIT[0])

    if user.needed_quests():

        if await quest_dispatcher(msg):

            quest = user.get_cur_quest()

            await msg.reply(quests_dops["dispatcher_true"])
            await welcome_to_the_Quest(user)
            await state.set_state(States_Quest.all()[quest.id_])

            return

        else:
            await msg.reply(quests_dops["dispatcher_false"])
            await state.set_state(States.GO_TO_NEXT[0])

    else:

        # Сохраняем всех, кто прошёл задания до конца.
        if user not in finished_quest:
            finished_quest.append(user)

        await tg_bot.send_video_note(id_, videos.dops["goodbye"])
        await msg.answer(quests_dops["win"].format(user.get_count_wins()))
        await state.set_state(States.GOODBYE[0])


@dispatcher.callback_query_handler(lambda c: c.data == "!run", state=States.GO_TO_NEXT)
async def processed_message(callback: types.CallbackQuery):

    id_ = callback.from_user.id
    user = list_user[id_]
    state = user.state

    await state.set_state(States.AWAIT[0])

    if user.needed_quests():

        if await quest_dispatcher(callback):

            quest = user.get_cur_quest()

            await tg_bot.send_message(id_, quests_dops["dispatcher_true"])
            await welcome_to_the_Quest(user)
            await state.set_state(States_Quest.all()[quest.id_])

            return

        else:
            await tg_bot.send_message(id_, quests_dops["dispatcher_false"])
            await state.set_state(States.GO_TO_NEXT[0])

    else:

        # Сохраняем всех, кто прошёл задания до конца.
        if user not in finished_quest:
            finished_quest.append(user)

        await tg_bot.send_video_note(id_, videos.dops["goodbye"])

        win_message_statistic = quests_dops["win"].format(user.get_count_wins())
        await tg_bot.send_message(id_, win_message_statistic)

        await state.set_state(States.GOODBYE[0])

##
####
##### =================================

@dispatcher.message_handler(state=States_Quest.QUEST_0)
async def q_Morze(msg: types.Message):

    id = msg.from_user.id
    user = list_user[id]
    name = user.name

    await user.state.set_state(States.AWAIT[0])

    coded = ''
    for char in name.lower():
        coded += code_Morze[char]

    user.morze = coded

    my_str = msg.text
    my_str = my_str.replace('…', '...')
    my_str = my_str.replace('—', '--')

    if my_str != coded:
        t = ''
        if len(my_str) < len(coded):
            for i in range(len(coded) - len(my_str)):
                my_str += '*'

        if len(my_str) > len(coded):
            my_str = my_str[:len(coded)]

        for i in range(len(coded)):
            if my_str[i] != coded[i]:
                t += '*'
            else:
                t += coded[i]

        videos_false = videos.dops["answer_false"]
        random_video = randint(0, len(videos_false) - 1)
        await tg_bot.send_video_note(id, videos_false[random_video])
        await sleep(time_await["video"])

        await msg.answer(text=f"Нет, что-то здесь не так. Попробуй еще раз. Звездочками обозначены "
                              f"места с ошибками.\n {t}")

        # Проверяем, нужна ли ему помощь пропустить квест.
        if user.get_counter_help() >= counter_help:

            await tg_bot.send_message(id, "Задание слишком сложное? Нажми кнопку \"Пропустить\".",
                                      reply_markup=Buttons["skip_quest"])

        else:
            user.up_counter_help()


    else:
        videos_true = videos.dops["answer_true"]
        random_video = randint(0, len(videos_true) - 1)
        await tg_bot.send_video_note(id, videos_true[random_video])

        await sleep(time_await["video"])
        await msg.answer(quests_dops["True"])

        # Блок кода - выход. Пользователь выходит из квеста, который затем отправляется по очереди.
        vacated_quest = quest_quit(user)
        vacated_user = await_user_dispatcher(vacated_quest)

        if vacated_user != False and vacated_quest != None:
            await tg_bot.send_message(vacated_user.id_, quests_dops["await_go"], reply_markup=Buttons["k_run"])


        await user.state.set_state(States.GO_TO_NEXT[0])

        await msg.answer(reg_start['start?'], reply_markup=Buttons["b_run"])
        return
        ###

    await user.state.set_state(States_Quest.QUEST_0[0])


@dispatcher.message_handler(state=States_Quest.all()[1:9:])
async def q_Quiz(msg: types.Message):

    id = msg.from_user.id
    user = list_user[id]
    state = user.state
    quest = user.get_cur_quest()

    await state.set_state(States.AWAIT[0])

    if await quest_processor(msg, quest.id_):

        # Блок кода - выход. Пользователь выходит из квеста, который затем отправляется по очереди.
        vacated_quest = quest_quit(user)
        vacated_user = await_user_dispatcher(vacated_quest)

        if vacated_user != False and vacated_quest != None:
            await tg_bot.send_message(vacated_user.id_, quests_dops["await_go"], reply_markup=Buttons["k_run"])

        await user.state.set_state(States.GO_TO_NEXT[0])

        await msg.answer(reg_start['start?'], reply_markup=Buttons["b_run"])
        return
        ###


    else:
        await user.state.set_state(States_Quest.all()[quest.id_])


@dispatcher.message_handler(state=States_Quest.QUEST_9, content_types=types.ContentType.ANY)
async def q_Photo(msg: types.Message):

    id_ = msg.from_user.id
    user = list_user[id_]
    state = user.state
    quest = user.get_cur_quest()

    await state.set_state(States.AWAIT[0])

    if len(msg.photo) > 0:

        await msg.reply("Да у тебя талант!")

        # Блок кода - выход. Пользователь выходит из квеста, который затем отправляется по очереди.
        vacated_quest = quest_quit(user)
        vacated_user = await_user_dispatcher(vacated_quest)

        if vacated_user != False and vacated_quest != None:
            await tg_bot.send_message(vacated_user.id_, quests_dops["await_go"], reply_markup=Buttons["k_run"])

        await user.state.set_state(States.GO_TO_NEXT[0])

        await msg.answer(reg_start['start?'], reply_markup=Buttons["b_run"])
        return
        ###


    await msg.reply("Я хочу увидеть фотографию твоего рисунка.")
    await state.set_state(States_Quest.QUEST_9[0])


@dispatcher.callback_query_handler(lambda c: c.data == "!reg")
async def register_user_by_button(callback_query: types.CallbackQuery):
    """
    Активация регистрации пользователя: по кнопке.
    """

    id = callback_query.from_user.id

    if id in pre_register_user and id not in list_user.keys():
        await register(callback_query)


@dispatcher.message_handler(state=States.REGISTER)
async def register_user(msg: types.Message):
    """
    Регистрация пользователей.

    :param msg:
    :return:
    """

    id = msg.from_user.id

    # print(list_user)

    state = list_user[id].state
    await state.set_state(States.AWAIT[0])

    if msg.text.lower() == button_text['reg_yes'].lower() and list_user[id].name != None:

        await tg_bot.send_video_note(id, Video_Notes().dops["hello_go"], reply_markup=types.ReplyKeyboardRemove())
        await sleep(time_await["video"])

        await msg.answer(welcome_start['start_game'], reply_markup=Buttons["k_run"])
        await sleep(time_await["text"])

        # await msg.answer(reg_start['go?'], reply_markup=Buttons["k_run"]),
        await msg.answer(reg_start['start?'],
                         reply_markup=Buttons["b_run"])

        print(f"Зарегистрирован пользователь: {list_user[id].name}")

        list_user[id].register = True


        await state.set_state(States.GO_TO_NEXT[0])  # перенаправление пользователей по заданиям.
        return


    elif msg.text.lower() == button_text['reg_no'].lower():
        await msg.answer(welcome_start['reg_ask_name'])
        list_user[id].name = None

    else:

        filter_name = re.sub(r'[^\w\s]+|[\d]+', '', msg.text).strip()

        for c in filter_name.lower():
            if c not in filter_char_name:

                list_user[id].name = None
                await msg.reply("В твоём имени должны быть только буквы кириллицы. Попробуй ещё раз!")
                await state.set_state(States.REGISTER[0])
                return

        if len(filter_name) <= 1:

            list_user[id].name = None
            await msg.reply("В твоём имени должно быть не менее 2х букв кириллицы. Попробуй ещё раз.")
            await state.set_state(States.REGISTER[0])
            return

        if filter_name.lower() == "да":

            list_user[id].name = None
            await msg.reply("Как тебя зовут?")
            await state.set_state(States.REGISTER[0])
            return

        else:

            list_user[id].name = filter_name

            await tg_bot.send_message(id, "Убедись, что твоё имя написано правильно.")
            await sleep(time_await["text"])

            await msg.reply(f"Тебя зовут {list_user[id].name}, верно?", reply_markup=Buttons['b_regs'])

            await state.set_state(States.REGISTER[0])
            return

    await state.set_state(States.REGISTER[0])


@dispatcher.message_handler()
async def process_user_answer(msg: types.Message):
    """
    Обработчик различных сообщений при нулевом состоянии.

    :param msg:
    :return:
    """

    if msg.from_user.id in pre_register_user:

        await register(msg)
        return

    await msg.reply("Для начала работы введи команду: /start", reply_markup=types.ReplyKeyboardRemove())


async def infinity_loop():
    """
    Очищает список прошедших пользователей.
    :return:
    """

    while True:

        await sleep(60)

        curtime = time()

        copy_users = copy(list_user)
        # users_completed = filter(lambda u: copy_users[u].needed_quests() == False, copy_users)
        users_await = (filter(lambda u: copy_users[u].register, copy_users))
        # print(users_await)
        #
        #
        # for u in users_completed:
        #
        #     print("Ожидает удаления: ", u)
        #
        #     if list_user[u].get_last_time_active() > curtime - 9:
        #         list_user.pop(u)
        #
        #         print("Удалён пользователь: ", u)

        for u in users_await:
            # print("Ожидает удаления: ", u)

            user = list_user[u]
            last_time_active = user.get_last_time_active()
            user_quest = user.get_cur_quest()
            state = user.state

            if last_time_active < curtime - timeout and user_quest == None:

                await state.set_state(States.AWAIT[0])

                # Блок кода - выход. Пользователь выходит из квеста, который затем отправляется по очереди.
                vacated_quest = quest_quit(user)
                vacated_user = await_user_dispatcher(vacated_quest)

                if vacated_user != False and vacated_quest != None:
                    await tg_bot.send_message(vacated_user.id_, quests_dops["await_go"], reply_markup=Buttons["k_run"])

                await state.reset_state()
                list_user.pop(u)
                print("Удалён пользователь: ", u)


async def logging():

    while True:

        await sleep(60)
        # Уведомление администратору об прохождении квестов.

        curTimeDay = datetime.datetime.today()
        if datetime.time(18) < curTimeDay.time() < datetime.time(18, 2):

            log_message = f"""Отчёт на {curTimeDay}. Прошло заданий: {len(finished_quest)} человек."""
            log_message += "\n\n"

            for u in finished_quest:
                log_message += f"{u.name}, {u.username}, попыток: {u.get_count_wins()}\n"

            await tg_bot.send_message(id_admin, log_message)
            finished_quest.clear()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.create_task(infinity_loop())
    loop.create_task(logging())
    asyncio.set_event_loop(loop)

    executor.start_polling(dispatcher)