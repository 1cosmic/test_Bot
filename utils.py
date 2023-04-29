from aiogram import Dispatcher, Bot

from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware



class TestStates(Helper):
    mode = HelperMode.shake_case

    TEST_STATE_0 = ListItem()
    TEST_STATE_1 = ListItem()


if __name__ == "__main__":
    bot = Bot()

    dp = Dispatcher(bot, storage=MemoryStorage())