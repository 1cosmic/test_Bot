
count_quest = 9
count_hints = 2


class User:
    def __init__(self, chatId, username, name, state):
        self.chatId = chatId  # id-чата
        self.username = username  # никнейм в телеграме.
        self.name = name  # имя человека при регистрации.
        self.state = state  # состояние dispatcher`а.

        self.__required_quests = list(range(count_quest))  # список квестов для прохождения
        self.__current_quest = None
        self.__counter_of_attemps = 0


    def get_counter(self):
        return self.__counter_of_attemps


    def reset_counter(self):
        self.__counter_of_attemps = 0


    def up_counter(self):
        self.__counter_of_attemps += 1


    def set_cur_quest(self, quest):
        self.__current_quest = quest


    def get_cur_quest(self):
        return self.__current_quest


    def is_free(self):
        """
        Проверяет, остались ли ещё квесты для прохождения.
        """

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

        return True


    def required_quests(self):
        return self.__required_quests



class Users_List():

    def __init__(self):
        self.__list_user = []
        self.__max_in_game = 8

    def addUser(self, user):
        if self.__max_in_game <= 8:
            self.__list_user.append(user)
            return True

        else:
            print("WARNING! \nMax user in game!")
            return False

    def removeUser(self, user):
        self.__list_user.remove(user)


    def getCountUsers(self):
        return len(self.__list_user)


    def getUsers(self):
        return self.__list_user


class Users_In_Game(Users_List):
    pass

class Users_Wait_Game(Users_List):
    pass