import utils
from test_states import TestStates

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor


bot = Bot("6188730051:AAE8M8uIeORLKb7mo5vUW0TAthTq4rvb9ts")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(state='*', commands=['setstate'])
async def setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)

    if not argument:
        await state.reset_state()
        return await message.reply("Состояние бота сброшено.")

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply("Ни один из ключей не подходит.")

    await state.set_state()



@dp.message_handler(state=TestStates.TEST_STATE_0)
async def state_first(msg: types.Message):
    await msg.reply("Состояние изменено. Текущее: 1.")


@dp.message_handler(commands=['start'])
async def test_start_command(message: types.Message):
    await message.reply("Тестовый запуск.")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == "__main__":
    executor.start_polling(dp)