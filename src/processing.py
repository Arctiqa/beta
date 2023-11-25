import re
from collections import Counter
import json


def get_dicts_not_executed(dict_list: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Возвращает список словарей, отсортированных по значению state
    :param dict_list: [{'id': 'идентификатор', 'state': 'состояние', 'date': 'дата'}]
    :param state: состояние платежа
    :return: отсортированный список по значению 'state'
    """
    sorted_list = []
    for dict_ in dict_list:
        if dict_.get('state') == state:
            sorted_list.append(dict_)
    return sorted_list


def get_dicts_sorted_by_date(dict_list: list[dict], sort_type: bool = True) -> list[dict]:
    """
    Возвращает отсортированый по убыванию/возрастанию даты список словарей
    :param dict_list: [{'id': 'идентификатор', 'state': 'состояние', 'date': 'дата'}]
    :param sort_type: возрастание/убывание
    :return: отсортированный список по значению 'date'
    """
    new_list = sorted(dict_list, key=lambda dict_: str(dict_.get('date', '')), reverse=sort_type)
    return new_list


def searching_description(dict_list, search_str=''):
    """
    Принимает список словарей с данными о банковских операциях и строку
    поиска и возвращает список словарей, у которых в описании есть данная строка
    :param dict_list: список словарей
    :param search_str: поисковый запрос
    :return: список транзакций с подходящим описанием поиска
    """

    return [dct for dct in dict_list if re.findall(search_str, str(dct.get('description', '')), flags=re.I)]


def dict_counter_by_description(dict_list, descriptions_dct):
    """
    Принимает список словарей с данными о банковских операциях и словарь категорий операций и возвращать словарь,
    в котором ключи — это названия категорий, а значения — это количество операций в каждой категории
    :param dict_list: список банковских операций в виде словаря
    :param descriptions_dct: Словарь с операциями вида {"название операции": 0}
    :return: descriptions_dct с количеством заданных в descriptions_dct операций
    """

    sorted_dict = Counter(dct["description"] for dct in dict_list
                          if dct.get("description", '') in descriptions_dct.keys())
    return dict(sorted_dict)

# with open(r'../data/operations.json', 'r', encoding='utf-8') as f:
#     lst = json.load(f)
# s = {'Перевод организации': 0, 'Перевод с карты на карту': 0,
#      'Перевод с карты на счет': 0, 'Перевод со счета на счет': 0}
# f = dict_counter_by_description(lst, s)
# print(f)
