from aiogram.utils.helper import Helper, HelperMode, ListItem

class States(Helper):
    """
    Системные состояния пользователей.
    """

    mode = HelperMode.snake_case

    REGISTER = ListItem()
    AWAIT = ListItem()
    AWAIT_QUEST = ListItem()
    GO_TO_NEXT = ListItem()
    GOODBYE = ListItem()


class States_Quest(Helper):
    """
    Состояния пользователей в квестах.
    """

    QUEST_0 = ListItem()  # Азбука Морзе.
    QUEST_1 = ListItem()
    QUEST_2 = ListItem()
    QUEST_3 = ListItem()
    QUEST_4 = ListItem()
    QUEST_5 = ListItem()
    QUEST_6 = ListItem()
    QUEST_7 = ListItem()
    QUEST_8 = ListItem()
    QUEST_9 = ListItem()  # Натюрморт.


code_Morze = {'а': '.-', 'б': '-...', 'в': '.--', 'г': '--.', 'д': '-..', 'е': '.', 'ё': '.',
             'ж': '...-', 'з': '--..', 'и': '..', 'й': '.---', 'к': '-.-', 'л': '.-..',
             'м': '--', 'н': '-.', 'о': '---', 'п': '.--.', 'р': '.-.', 'с': '...', 'т': '-',
             'у': '..-', 'ф': '..-.', 'х': '....', 'ц': '-.-.', 'ч': '---.', 'ш': '----',
             'щ': '--.-', 'ъ': '.--.-.', 'ь': '-..-', 'ы': '-.--', 'э': '..-..', 'ю': '..--',
             'я': '.-.-',
             }
