import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Простой пагинатор
class Paginator:
    """ Класс для работы с пагинацией """
    def __init__(self, array: list | tuple, page: int=1, per_page: int=1, pattern: int=10):
        self.array = array
        self.per_page = per_page
        self.page = page
        self.pattern = pattern 
        self.len = len(self.array)
        # math.ceil - округление в большую сторону до целого числа
        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self):
        """ функция получения среза массива """
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        """ Плоучение текущей страницы """
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        """ Проверяет, есть ли следующая страница после текущей """
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self):
        """ Проверяет, есть ли предыдущая страница перед текущей """
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        """ Функция получения следующей страницы """
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError('Next page does not exist. Use has_next() to check before.')

    def get_previous(self):
        """ Функция получения предыдущей страницы """
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError('Previous page does not exist. Use has_previous() to check before.')