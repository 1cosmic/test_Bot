import random

from new_upload_videos import config

from project.users import User
from project.buttons import Buttons
from project.utils import States, States_Quest, code_Morze
from project.video_notes import Video_Notes
from project.skeleton_quest import create_quests, free_quests
from project.messages import quests_welcomes, quests_answers, quests_dops, quests_hints, welcome_start

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from asyncio import sleep

# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# =-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-=
# Функции для внутренней работы программы (автоматизаторы).

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
        await state.set_state(States.REGISTER[0])

        list_user[id] = User(id, username, None, state)

        await tg_bot.send_video_note(id, videos.dops["hello_start"])
        await sleep(5)

        await tg_bot.send_message(id, welcome_start['reg_ask_name'], reply_markup=types.ReplyKeyboardRemove())


    # Создаём список квестов для прохождения.
    list_quest = create_quests()


    async def go_to_next_quest(user=None, quest=None):

        if user == None:

            for u in await_user:
                user = list_user[u]
                id = quest.id

                if id in user.required_quests():
                    await tg_bot.send_message(user.chatId, "Перенаправляю на следующий квест...")

                    # Удаляем пользователя из очереди ожидающих.
                    await_user.remove(u)

                    # Связываем пользователя и его квест.
                    list_quest[id].occupy(user)
                    user.set_cur_quest(quest)

                    # Устанавливаем состояние пользователя на прохождение соответствующего квеста.
                    # cur_state = dispatcher.current_state(user=u)
                    # await cur_state.set_state(States_Quest.all()[id])
                    await user.state.set_state(States_Quest.all()[id])

                    # DEBUG:
                    # await tg_bot.send_message(user.chatId, f"Твоё текущее состояние: {await user.state.get_state()}")
                    await welcome_to_the_Quest(user, quest.id)

        if quest == None:

            print("Пытаюсь обработать пользователя.")

            for q in free_quests(list_quest):

                if q.id in user.required_quests():
                    print("Сейчас пользователь будет перенаправлен.")

                    # Связываем пользователя и его квест.
                    # quest_id = list_quest.index(q)
                    list_quest[q.id].occupy(user)
                    user.set_cur_quest(q)

                    # Устанавливаем состояние пользователя на прохождение соответствующего квеста.
                    state = dispatcher.current_state(user=user.chatId)
                    await state.set_state(States_Quest.all()[q.id])

                    # Уведомляем пользователя об переходе на следующий квест.
                    await tg_bot.send_message(user.chatId, f"Перенаправляю на следующий квест: {q.name}")
                    await welcome_to_the_Quest(user, q.id)

                    # DEBUG:
                    # await tg_bot.send_message(user.chatId, f"Твоё текущее состояние: {await state.get_state()}")

                    return True

        return False


    async def check_of_free_quests(id):
        """
        Функция распределения пользователей по комнатам-квестам.

        :param message:
        :return:
        """

        user = list_user[id]

        if user.is_free():
            if id not in await_user:

                # await tg_bot.send_message(id, "Сейчас проверим, свободны ли квесты?")
                await sleep(1.5)

                if len(free_quests(list_quest)) > 0:
                    # await tg_bot.send_message(id, "По идее, сейчас я тебя перенаправлю на другой квест. Ожидай.",
                    # reply_markup=types.ReplyKeyboardRemove())

                    await go_to_next_quest(user=user)

                else:
                    if id not in await_user:
                        await_user.append(id)

                    await tg_bot.send_message(id,
                                              "Погоди немного, сейчас освободится локация и я тебя проведу к ней. Держи телефон при себе!")

            else:
                await tg_bot.send_message(id, "Перед тобой в очереди 1 человек. Подожди немного, сейчас "
                                              "он закончит и мы продолжим.")

        else:
            state = list_user[id].state

            await tg_bot.send_video_note(id, videos.dops["goodbye"])
            await tg_bot.send_message(id, "Ты успешно прошёл все комнаты! Покажи это сообщение администратору и получи "
                                          "свой подарок!")

            await state.set_state(States.GOODBYE[0])


    async def quit_from_quest(user):

        state = user.state

        # Освобождаем квест.
        quest = user.get_cur_quest()
        list_quest[quest.id].free()

        # Очищаем данный квест из непрошедних пользоватем и устанавливаем текущий - None.
        user.pop_quest(quest.id)
        user.set_cur_quest(None)
        user.reset_counter()

        # await msg.answer(f"Твоё текущее состояние: {await state.get_state()}")
        await state.set_state(States.GO_TO_NEXT[0])

        # Отправляем освободившийся квест дальше по очереди.
        await go_to_next_quest(quest=quest)

        # Перенаправляем юзера, освободившего квест.
        await tg_bot.send_message(user.chatId,
                                  "Сейчас я отправлю тебя на следующий квест.",
                                  reply_markup=Buttons['k_run'])
        await tg_bot.send_message(user.chatId, "Готов?", reply_markup=Buttons['b_run'])


    async def welcome_to_the_Quest(user, id_quest):

        await sleep(1)

        for video in videos.question[id_quest]:
            print(video)
            await tg_bot.send_video_note(user.chatId, video)
            await sleep(5)

        await tg_bot.send_message(user.chatId, quests_welcomes[id_quest], reply_markup = types.ReplyKeyboardRemove())


    async def quest_processor(id, msg, id_quest):

        user = list_user[id]

        print(f"Попытка пользователя № {user.get_counter()}")

        if msg.text == quests_answers[id_quest]:

            videos_true = videos.dops["answer_true"]
            random_video = random.randint(0, len(videos_true) -1)

            await tg_bot.send_video_note(id, videos_true[random_video])
            await sleep(1.5)

            await msg.answer(quests_dops["True"])
            await sleep(1)

            return True

        else:

            flag_for_hints = user.get_counter()
            if flag_for_hints < 2:

                user.up_counter()

                videos_false = videos.dops["answer_false"]
                random_video = random.randint(0, len(videos_false) -1)

                await tg_bot.send_video_note(id, videos_false[random_video])
                await sleep(1.5)
                await msg.answer(quests_dops["False"])
                await sleep(1)

                await tg_bot.send_video_note(id, videos.hint[id_quest][flag_for_hints])
                await sleep(1.5)
                await msg.reply(quests_hints[id_quest][flag_for_hints])
                await sleep(1)

            else:
                print("Дописать логику: при превышении числа подсказок.")
                return False


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
            await tg_bot.send_message(id, "Тебя ждёт увлекательное приключение!", reply_markup=Buttons['b_start'])

            return True

        if id in list_user.keys():
            await message.answer("Ты уже зарегистрирован. Продолжай прохождение!")

        # Чистим историю диалога, если человек вышел за границы наших возможностей и познал Дзен.
        # await tg_bot.delete_message(message.chat.id, message.message_id)


    @dispatcher.callback_query_handler(lambda c: c.data == "!reg")
    async def register_user_by_button(callback_query: types.CallbackQuery):
        """
        Активация регистрации пользователя: по кнопке.

        :param callback_query:
        :return:
        """

        id = callback_query.from_user.id
        username = callback_query.from_user.username

        if id in pre_register_user:
            await register(id, username)


    @dispatcher.callback_query_handler(lambda c: c.data == "!run", state=States.GO_TO_NEXT)
    async def processed_message(msg: types.Message):

        await msg.answer("Кнопка обработана.")
        user = msg.from_user.id
        await check_of_free_quests(user)


    @dispatcher.message_handler(state=States_Quest.all(), commands=['quit'])
    async def quit_from_game(msg: types.Message):
        """
        Выход из игры.

        :param message:
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

        user = msg.from_user.id
        # state = dispatcher.current_state(user = user)
        # await msg.answer(f"Твоё текущее состояние в хэндлере GO_TO_NEXT: {await state.get_state()}")

        await check_of_free_quests(user)


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

        for char in name.lower():
            coded += code_Morze[char]

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
            random_video = random.randint(0, len(videos_false) -1)
            await tg_bot.send_video_note(id, videos_false[random_video])
            await sleep(1.5)

            await msg.answer(text=f"Нет, что-то здесь не так. Попробуй еще раз. Звездочками обозначены "
                                  f"места с ошибками.\n {t}")
            return

        else:
            videos_true = videos.dops["answer_true"]
            random_video = random.randint(0, len(videos_true) -1)
            await tg_bot.send_video_note(id, videos_true[random_video])
            await sleep(1.5)

            await msg.answer(text="Молодец! Все верно!\nКвест пройден!")
            await quit_from_quest(user=user)




    @dispatcher.message_handler(state=States_Quest.all()[1::])
    async def q_Quiz(msg: types.Message):

        id = msg.from_user.id
        user = list_user[id]
        quest = user.get_cur_quest()

        if await quest_processor(id, msg, quest.id):
            # await msg.reply(quests_dops["True"])
            await quit_from_quest(user)


    @dispatcher.message_handler(state=States.REGISTER)
    async def register_user(msg: types.Message):
        """
        Регистрация пользователей.

        :param msg:
        :return:
        """

        id = msg.from_user.id
        state = list_user[id].state

        if msg.text == "Да" and list_user[id].name != None:

            await msg.answer("Отлично! Мы готовы начинать.", reply_markup=types.ReplyKeyboardRemove())

            await tg_bot.send_video_note(id, Video_Notes().dops["hello_go"])
            await sleep(10)

            await msg.answer("Ну что, начнём приключения?", reply_markup=Buttons["k_run"]),
            await msg.answer("Как только ты будешь готов, нажми кнопку и мы приступим!",
                             reply_markup=Buttons["b_run"])

            # Включить после написания готовой логики распределения по квестам.
            await state.set_state(States.GO_TO_NEXT[0])  # распределение по алгоритму.
            # await state.set_state(States.AWAIT_QUEST[0])  # распределение по кнопке.

        elif msg.text == "Нет":
            await msg.answer(welcome_start['reg_ask_name'])
            list_user[id].name = None

        else:
            list_user[id].name = msg.text

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

        await msg.reply("Для начала работы введи команду: /start")
        # await msg.reply(f"Your ID: {id}")


    executor.start_polling(dispatcher)
