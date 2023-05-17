from random import shuffle, randint
import re

from project import config

from project.users import User
from project.buttons import Buttons, button_text, Buttons_answers
from project.utils import States, States_Quest, code_Morze
from project.video_notes import Video_Notes
from project.skeleton_quest import create_quests, free_quests, user_in_quests
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

# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=

if __name__ == "__main__":

    ### ==========

    # Для инициализации токена необходимо вбить его вместо config.TOKEN.
    # Однако, если вы хотите работать в команде и с git`ом, то лучше заведите файл config,
    # в котором создайте переменную TOKEN и присвойте ей значение вашего TG-бота.
    token = config.TOKEN
    videos = Video_Notes()

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


    async def register(id, username):

        pre_register_user.remove(id)

        state = dispatcher.current_state(user=id)
        await state.set_state(States.AWAIT[0])

        list_user[id] = User(id, username, None, state)

        await tg_bot.send_video_note(id, videos.dops["hello_start"], reply_markup=types.ReplyKeyboardRemove())
        await sleep(5)

        await tg_bot.send_message(id, welcome_start["reg"])
        await sleep(1)
        await tg_bot.send_message(id, welcome_start['reg_ask_name'])

        await state.set_state(States.REGISTER[0])


    # Создаём список квестов для прохождения.
    list_quest = create_quests()


    async def go_to_next_quest(user=None, quest=None):

        if user == None:

            for u in await_user:
                user = list_user[u]
                id = quest.id

                if id in user.required_quests():
                    await tg_bot.send_message(user.chatId, "Перенаправляю на следующее задание...",
                                              reply_markup=types.ReplyKeyboardRemove())

                    # Удаляем пользователя из очереди ожидающих.
                    await_user.remove(u)

                    # Связываем пользователя и его квест.
                    list_quest[id].occupy(user)
                    user.set_cur_quest(quest)

                    # cur_state = dispatcher.current_state(user=u)
                    # await cur_state.set_state(States_Quest.all()[id])

                    # DEBUG:
                    # await tg_bot.send_message(user.chatId, f"Твоё текущее состояние: {await user.state.get_state()}")

                    await user.state.set_state(States.AWAIT[0])
                    await welcome_to_the_Quest(user, quest.id)

                    # Устанавливаем состояние пользователя на прохождение соответствующего квеста.
                    await user.state.set_state(States_Quest.all()[id])

                    # DEBUG 1:
                    print(f"Пользователь {user.username} удалён из очереди ожидающих: {await_user}")

                    return

        if quest == None:

            # print("Пытаюсь обработать пользователя.")

            quests = free_quests(list_quest)

            # Мешаем содержимое списка, рандомизируя порядок квестов.
            shuffle(quests)

            for q in quests:

                if q.id in user.required_quests():
                    # print("Сейчас пользователь будет перенаправлен.")

                    # Связываем пользователя и его квест.
                    # quest_id = list_quest.index(q)
                    list_quest[q.id].occupy(user)
                    user.set_cur_quest(q)

                    # await tg_bot.send_message(user.chatId, f"Перенаправляю на следующее задание: {q.name}",
                    #                           reply_markup=types.ReplyKeyboardRemove())

                    # Устанавливаем состояние пользователя на прохождение соответствующего квеста.
                    await user.state.set_state(States.AWAIT[0])

                    await welcome_to_the_Quest(user, q.id)

                    state = user.state
                    # print(q.id)
                    await state.set_state(States_Quest.all()[q.id])

                    # Уведомляем пользователя об переходе на следующий квест.

                    # DEBUG:
                    # await tg_bot.send_message(user.chatId, f"Твоё текущее состояние: {await state.get_state()}")

                    return True

        return False


    async def check_of_free_quests(id):
        """
        Функция распределения пользователей по комнатам-квестам.

        # :param message:
        :return:
        """

        user = list_user[id]
        state = list_user[id].state

        print(f"Пользователь {user.name} пытается перейти на следующий квест. Ему осталось {len(user.required_quests())} квест/ов.")

        if user.is_free():

            print(f"Пользователю {user.name} ещё необходимо пройти задания.")

            if id not in await_user:

                print(f"Пользователь {user.name} не в списке ожидающих.")

                # await tg_bot.send_message(id, "Сейчас проверим, свободны ли квесты?")
                await sleep(1.5)

                if len(free_quests(list_quest)) > 0:
                    # await tg_bot.send_message(id, "По идее, сейчас я тебя перенаправлю на другой квест. Ожидай.",
                    # reply_markup=types.ReplyKeyboardRemove())
                    print(f"Перенаправляю пользователя {user.name} на следующий квест.")

                    await go_to_next_quest(user=user)

                    return

                else:
                    if id not in await_user:
                        await_user.append(id)

                    await tg_bot.send_message(id,
                                              "Погоди немного, сейчас освободится задание и я тебя проведу к нему. Держи телефон при себе!")

            else:
                await tg_bot.send_message(id, "Перед тобой в очереди 1 человек. Подожди немного, сейчас "
                                              "он закончит и мы продолжим.")


            print(f"Пользователь {user.name} В списке ожидающих.")

        else:

            await tg_bot.send_video_note(id, videos.dops["goodbye"])
            await tg_bot.send_message(id, "Ты успешно прошёл все задания! Покажи это сообщение администратору и получи "
                                          "свой подарок!")

            await tg_bot.send_message(id, "Всего пройдено заданий: {} / 10.".format(user.get_count_wins()))

            await state.set_state(States.GOODBYE[0])

            return

        await state.set_state(States.GO_TO_NEXT[0])


    async def quit_from_quest(user):

        state = user.state
        await state.set_state(States.AWAIT[0])

        # Освобождаем квест.
        quest = user.get_cur_quest()
        list_quest[quest.id].free()

        # Очищаем данный квест из непрошедних пользоватем и устанавливаем текущий - None.
        user.pop_quest(quest.id)
        user.set_cur_quest(None)
        user.reset_counter_attemps()
        user.reset_counter_help()

        # Отправляем освободившийся квест дальше по очереди.
        await go_to_next_quest(quest=quest)

        # await msg.answer(f"Твоё текущее состояние: {await state.get_state()}")
        await state.set_state(States.GO_TO_NEXT[0])

        # Перенаправляем юзера, освободившего квест.
        await tg_bot.send_message(user.chatId,
                                  "Сейчас я отправлю тебя на следующее задание.",
                                  reply_markup=Buttons['k_run'])
        await tg_bot.send_message(user.chatId, "Готов?", reply_markup=Buttons['b_run'])

        name_quests = [i.name for i in list_quest]
        print(f"Пользователь {user.username} прошёл квест {quest.name}. Список свободных квестов: {name_quests}")


    async def welcome_to_the_Quest(user, id_quest):

        await sleep(1)


        for video in videos.question[id_quest]:
            # print(video)
            await tg_bot.send_video_note(user.chatId, video)
            await sleep(4)

        await tg_bot.send_message(user.chatId, quests_welcomes[id_quest].format(user.name),
                                  reply_markup=types.ReplyKeyboardRemove())

        if id_quest in range(6, 9):
            await sleep(1)
            await tg_bot.send_message(user.chatId, "Выбери правильный ответ.", reply_markup=Buttons_answers.restruct())



    async def quest_processor(id, msg, id_quest):

        user = list_user[id]
        # msg.reply("Test: ", reply_markup=Buttons_answers.keyboard)

        # print(f"Попытка пользователя № {user.get_counter_attemps()}")

        if msg.text.lower() == quests_answers[id_quest]:

            videos_true = videos.dops["answer_true"]
            random_video = randint(0, len(videos_true) - 1)

            await tg_bot.send_video_note(id, videos_true[random_video])
            await sleep(1.5)

            await msg.answer(quests_dops["True"])
            await sleep(1)
            #
            return True

        else:
            # Отправляем нужную подсказку в соответствии с числом попыток.
            if user.get_counter_attemps() >= 2:
                user.reset_counter_attemps()

            flag_for_hints = user.get_counter_attemps()

            videos_false = videos.dops["answer_false"]
            random_video = randint(0, len(videos_false) - 1)

            await tg_bot.send_video_note(id, videos_false[random_video])
            await sleep(1.5)
            await msg.answer(quests_dops["False"])
            await sleep(1)

            if id_quest in videos.hint.keys():
                if flag_for_hints < len(videos.hint[id_quest]):

                    await tg_bot.send_video_note(id, videos.hint[id_quest][flag_for_hints])
                    await sleep(1.5)

            if id_quest in quests_hints.keys():
                await msg.reply(quests_hints[id_quest][flag_for_hints])
                await sleep(1)

            user.up_counter_attemps()

            # # Если квест с 6 по 8 - даём выбор правильных ответов.
            # if id_quest in range(6, 9):
            #
            #     await msg.answer("Выбери правильный ответ.", reply_markup=Buttons_answers.restruct())
            #     # print(range(6, 9))

            # Проверяем, нужна ли ему помощь пропустить квест.
            if user.get_counter_help() >= counter_help:

                await tg_bot.send_message(id, "Задание слишком сложное? Нажми кнопку \"Пропустить\".",
                                          reply_markup=Buttons["skip_quest"])

            else:
                user.up_counter_help()

        # id_quest = user.get_cur_quest().id
        # await user.state.set_state(States_Quest.all()[id_quest])


    # =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
    # =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
    # =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
    # =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
    # =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
    # =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=

    @dispatcher.message_handler(state=States.GOODBYE)
    async def goodbye(msg: types.Message):
        await msg.reply("Ты успешно прошёл все испытания! Скорее подходи к администратору музея, мы ждём тебя ;)")


    @dispatcher.message_handler(state='*', commands=['start'])
    async def start(message: types.Message):

        # TODO: Изменить приветствие, добавить медиа и т.п.
        id = message.from_user.id

        # Добавляем пользователя в очередь на регистрацию.
        if (id not in pre_register_user) and (id not in list_user.keys()):
            pre_register_user.append(id)

            # Приветствие.

            await message.answer(welcome_start['hello'], reply_markup=Buttons['k_start'])
            # await sleep(1)
            await tg_bot.send_message(id, welcome_start['hello_2'], reply_markup=Buttons['b_start'])

            return True

        if id in list_user.keys():
            await message.answer("Ты уже зарегистрирован. Продолжай прохождение!")

        # Чистим историю диалога, если человек вышел за границы наших возможностей и познал Дзен.
        # await tg_bot.delete_message(message.chat.id, message.message_id)


    @dispatcher.message_handler(state="*", commands=["restart"])
    async def restart_game_for_user(msg: types.Message):
        """
        Сбрасывает все состояния пользовател, переводя его в режим регистрации.
        :param msg:
        :return:
        """

        id = msg.from_user.id

        if user_in_quests(list_quest, id):
            user = list_user[id]
            quest_id = user.get_cur_quest().id

            list_quest[quest_id].free()
            await go_to_next_quest(quest_id)

        if id in list_user.keys():
            await list_user[id].state.reset_state()
            list_user.pop(id)

        if id in pre_register_user:
            pre_register_user.remove(id)


    @dispatcher.message_handler(state=States.AWAIT)
    async def wait(msg: types.Message):
        pass


    @dispatcher.callback_query_handler(lambda c: c.data == "!reg")
    async def register_user_by_button(callback_query: types.CallbackQuery):
        """
        Активация регистрации пользователя: по кнопке.

        :param callback_query:
        :return:
        """

        id = callback_query.from_user.id
        username = callback_query.from_user.username

        if id in pre_register_user and id not in list_user.keys():
            await register(id, username)


    @dispatcher.callback_query_handler(lambda c: c.data == "!run", state=States.GO_TO_NEXT)
    async def processed_message(msg: types.Message):

        await msg.answer("Смотрю, свободен ли путь...")

        user = msg.from_user.id
        await list_user[user].state.set_state(States.AWAIT[0])

        await check_of_free_quests(user)


    @dispatcher.callback_query_handler(lambda x: x.data == "!skip_quest", state=States_Quest.all())
    async def quit_from_game(msg: types.Message):
        """
        Выход из игры.
        """

        user_id = msg.from_user.id
        user = list_user[user_id]
        quest_id = user.get_cur_quest().id

        if user.get_counter_help() >= counter_help:

            # Убавляем счётчик личных побед пользователя.
            user.reduce_win()

            if await user.state.get_state() == States_Quest.QUEST_1[0]:
                answer = user.morze

            else:
                answer = quests_answers[quest_id]

            await tg_bot.send_message(user_id,
                                      f"Не печалься! В следующий раз обязательно получится 😉 \nПравильный ответ: {answer}")

            await quit_from_quest(user=user)

            return True



    @dispatcher.message_handler(state=States_Quest.all(), commands=['quit'])
    async def quit_from_game(msg: types.Message):
        """
        Выход из игры.

        :return:
        """

        await msg.answer("Выходим из квеста.")

        id = msg.from_user.id
        user = list_user[id]

        await quit_from_quest(user)

        return True


    ##### =================================
    ####
    ##
    # Обработка сигналов после регистрации -> старт прохождения квестов.

    @dispatcher.message_handler(state=States.GO_TO_NEXT)
    async def processed_message(msg: types.Message):

        id = msg.from_user.id
        user = list_user[id]

        await user.state.set_state(States.AWAIT[0])

        await check_of_free_quests(id)

    ##
    ####
    ##### =================================

    @dispatcher.message_handler(state=States_Quest.QUEST_1)
    async def q_Morze(msg: types.Message):

        # await msg.answer("Квест 1")

        id = msg.from_user.id
        user = list_user[id]
        name = user.name
        coded = ''

        await user.state.set_state(States.AWAIT[0])

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
            await sleep(1.5)

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
            await sleep(1.5)

            await msg.answer(text="Молодец! Все верно!\nКвест пройден!")
            await quit_from_quest(user=user)

            return

        await user.state.set_state(States_Quest.QUEST_1[0])


    @dispatcher.message_handler(state=States_Quest.all()[1:9:])
    async def q_Quiz(msg: types.Message):

        id = msg.from_user.id
        user = list_user[id]
        quest = user.get_cur_quest()

        await user.state.set_state(States.AWAIT[0])

        if await quest_processor(id, msg, quest.id):
            # await msg.reply(quests_dops["True"])
            await quit_from_quest(user)

        else:
            await user.state.set_state(States_Quest.all()[quest.id])


    @dispatcher.message_handler(state=States_Quest.QUEST_9, content_types=types.ContentType.ANY)
    async def q_Photo(msg: types.Message):

        id = msg.from_user.id
        user = list_user[id]
        quest = user.get_cur_quest()

        if len(msg.photo) > 0:
            await msg.reply("Да у тебя талант!")
            await quit_from_quest(user)

            return

        # else:
        await msg.reply("Я хочу увидеть фотографию твоего рисунка.")



    @dispatcher.message_handler(state=States.REGISTER)
    async def register_user(msg: types.Message):
        """
        Регистрация пользователей.

        :param msg:
        :return:
        """

        id = msg.from_user.id
        state = list_user[id].state

        if msg.text == button_text['reg_yes'] and list_user[id].name != None:

            await state.set_state(States.AWAIT[0])

            await tg_bot.send_video_note(id, Video_Notes().dops["hello_go"], reply_markup=types.ReplyKeyboardRemove())
            await sleep(5)

            await msg.answer(welcome_start['start_game'], reply_markup=Buttons["k_run"])
            await sleep(1)

            # await msg.answer(reg_start['go?'], reply_markup=Buttons["k_run"]),
            await msg.answer(reg_start['start?'],
                             reply_markup=Buttons["b_run"])


            await state.set_state(States.GO_TO_NEXT[0])  # распределение по алгоритму.

            # Включить после написания готовой логики распределения по квестам.
            # await state.set_state(States.AWAIT_QUEST[0])  # распределение по кнопке.

        elif msg.text == button_text['reg_no']:
            await msg.answer(welcome_start['reg_ask_name'])
            list_user[id].name = None

        else:

            filter_name = re.sub(r'[^\w\s]+|[\d]+', '', msg.text).strip()

            for c in filter_name.lower():
                if c not in filter_char_name:
                    list_user[id].name = None
                    await msg.reply("В твоём имени должны быть только буквы кириллицы. Попробуй ещё раз!")
                    return

            if len(filter_name) <= 1:
                await msg.reply("В твоём имени должно быть не менее 2х букв кириллицы. Попробуй ещё раз.")
                list_user[id].name = None

                return

            list_user[id].name = filter_name

            await tg_bot.send_message(id, "Убедись, что твоё имя написано правильно.")
            await sleep(1.5)

            await msg.reply(f"Тебя зовут {list_user[id].name}, верно?", reply_markup=Buttons['b_regs'])


    @dispatcher.message_handler()
    async def process_user_answer(msg: types.Message):
        """
        Обработчик различных сообщений при нулевом состоянии.

        :param msg:
        :return:
        """

        id = msg.from_user.id
        # state = dispatcher.current_state(user=msg.from_user.id)

        if msg.from_user.id in pre_register_user:
            return await register(id, msg.from_user.username)

        await msg.reply("Для начала работы введи команду: /start", reply_markup=types.ReplyKeyboardRemove())
        # await msg.reply(ascii_letters)
        # await msg.reply(f"Your ID: {id}")


    executor.start_polling(dispatcher)
