
from time import time

# count_quest = 2
# count_hints = 10



class User:
    def __init__(self, id_, username, name, state, count_quest):

        self.id_ = id_  # id-чата
        self.username = username  # никнейм в телеграме.
        self.name = name  # имя человека при регистрации.
        self.state = state  # состояние dispatcher`а.

        self.morze = None

        self.__required_quests = list(range(count_quest))  # список квестов для прохождения
        self.__current_quest = None
        self.__counter_of_attemps = 0
        self.__counter_of_help = 0

        self.__await = False

        self.__counter_wins = count_quest

        self.__last_time_active = time()
        self.register = False


    def get_counter_attemps(self):
        self.____last_time_activeve_time = time()
        return self.__counter_of_attemps


    def reset_counter_attemps(self):
        self.__last_time_active = time()
        self.__counter_of_attemps = 0


    def up_counter_attemps(self):
        self.__last_time_active = time()
        self.__counter_of_attemps += 1


    def get_counter_help(self):
        self.__last_time_active = time()
        return self.__counter_of_help


    def reset_counter_help(self):
        self.__last_time_active = time()
        self.__counter_of_help = 0


    def up_counter_help(self):
        self.__last_time_active = time()
        self.__counter_of_help += 1


    def set_cur_quest(self, quest):
        self.__last_time_active = time()
        self.__current_quest = quest


    def get_cur_quest(self):
        self.__last_time_active = time()
        return self.__current_quest


    def reduce_win(self):
        self.__last_time_active = time()
        self.__counter_wins -= 1

    def get_count_wins(self):
        self.__last_time_active = time()
        return self.__counter_wins

    def needed_quests(self):
        """
        Проверяет, остались ли ещё квесты для прохождения.
        """

        self.__last_time_active = time()

        if len(self.__required_quests) == 0:
            return False

        else:
            return True

    def pop_quest(self, id):
        """
        Удаляет квест чей id - в списке оставшихся для прохождения.

        :param id: int, номер квеста
        :return: True
        """

        # Удаляем данный квест из списка.
        self.__required_quests.remove(id)
        self.__last_time_active = time()

        return True


    def required_quests(self):
        self.__last_time_active = time()
        return self.__required_quests


    def get_last_time_active(self):
        return self.__last_time_active


    def setAwait(self, await_boolean):
        """Set await status."""
        self.__await = await_boolean

    def getAwait(self):
        """Return current await status."""
        return self.__await