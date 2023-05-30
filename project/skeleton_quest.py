
"""
Список всех квестов для их обработки, фильтрации и т.п. в основном коде.
"""

class Quest():
    def __init__(self, id_, name, type):

        self.id_ = id_
        self.name = name
        self.type = type

        self.__Users = {}


    def addUser(self, user):

        if user.id_ not in self.__Users.keys():
            self.__Users[user.id_] = user
            return True

        else:
            return False


    def removeUser(self, user):

        if user.id_ in self.__Users.keys():
            self.__Users.pop(user.id_)
            return True

        else:
            return False


    def getCountUser(self):
        return len(self.__Users)


def create_quests():
    """
    Создаём список квестов (для фильтрации по приоритетности).
    """

    res = list()

    # Заполняем список.
    res.append(Quest(0, "Азбука Морзе", "morze"))  # Азбука Морзе
    res.append(Quest(1, "Лаборатория света", "quest"))
    res.append(Quest(2, "Скорость вращения планеты", "quest"))
    res.append(Quest(3, "Диапроектор", "quest"))
    res.append(Quest(4, "Ракушка", "quest"))
    res.append(Quest(5, "Головоломка из Китая", "quest"))
    res.append(Quest(6, "Чемодан", "quest"))
    res.append(Quest(7, "Старый железный утюг", "quest"))
    res.append(Quest(8, "Звук ветра", "quest"))
    res.append(Quest(9, "Натюрморт", "quest"))
    #
    return res
