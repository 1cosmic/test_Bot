from aiogram import Dispatcher, Bot

from aiogram.utils.helper import Helper, HelperMode, ListItem



class TestStates(Helper):
    mode = HelperMode.snake_case

    TEST_STATE_0 = ListItem()
    TEST_STATE_1 = ListItem()

