
"""
Список всех квестов для их обработки, фильтрации и т.п. в основном коде.
"""

class Quest():
    def __init__(self, id, name, type, priority):

        self.id = id
        self.name = name
        self.type = type
        self.priority = priority

        self.__occupy_by_user = None  # занят пользователем = User()
        self.__free = True  # свободен ли для прохождения в настоящий момент


    def is_free(self):
        '''
        Если квест сейчас свободен - вернёт True.
        Иначе - False.
        '''

        return self.__free


    def occupy(self, user):
        """
        Занимает данный квест, если он свободен.
        """

        if self.__free == True:
            self.__free = False
            self.__occupy_by_user = user

            return True

        else:
            return False


    def free(self):
        '''
        Освобождает квест, если пользователь его прошёл.
        '''

        if self.__free == False:
            self.__free = True
            self.__occupy_by_user = None

            return True

        else:
            return False


def create_quests():
    """
    Создаём список квестов (для фильтрации по приоритетности).
    """

    res = list()

    # Заполняем список.
    res.append(Quest(0, "Азбука Морзе", "morze", 1))  # Азбука Морзе
    res.append(Quest(1, "Лаборатория света", "quest", 3))
    res.append(Quest(2, "Скорость вращения планеты", "quest", 3))
    res.append(Quest(3, "Диапроектор", "quest", 3))
    res.append(Quest(4, "Ракушка", "quest", 3))
    res.append(Quest(5, "Головоломка из Китая", "quest", 3))
    res.append(Quest(6, "Чемодан", "quest", 3))
    res.append(Quest(7, "Старый железный утюг", "quest", 3))
    res.append(Quest(8, "Звук ветра", "quest", 3))
    # res.append(Quest(9, "Натюрморт", "quest", 3))
    #...

    return res


def free_quests(quests_list):
    res = list(filter(lambda x: x.is_free(), quests_list))

    print_res = []
    for i in res:
        print_res.append(i.id)

    print("Вывожу результат фильтрации:", print_res)
    return res