import re

class StrRegular():
    """Класс для проверки строк с помощью регулярных выражений"""
    def __init__(self, txt: str):
        self.txt = txt
        
    @staticmethod
    async def contains_only_non_digits(txt: str) -> bool:
        """
        Проверяет, что строка содержит только символы и не содержит цифр.

        Аргументы:
        s (str): Входная строка для проверки.

        Возвращает:
        bool: True, если строка не содержит цифр, иначе False.

        Примеры:
        >>> contains_only_non_digits("Привет")
        True
        >>> contains_only_non_digits("Hello123")
        False
        """
        pattern = r'^[A-Za-zА-Яа-яЁё\s]+$'
        return bool(re.match(pattern, txt))