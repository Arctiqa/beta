from typing import Generator


def filter_by_currency(transact: list[dict], currency: str) -> Generator:
    """
    Функция выдает значения из генератора списка словарей по выбранной валюте
    :param transact: список словарей с данными о транзакциях
    :param currency: валюта платежа
    :return: значение из генератора списка словарей по выбранной валюте
    """
    for dct in transact:
        if dct["operationAmount"]["currency"]["code"] == currency:
            yield dct


def transaction_descriptions(transact: list[dict]) -> Generator:
    """
    Функция по очереди выводит описание произведенной операции
    :param transact: список словарей с данными о транзакциях
    :return: назначение проведенной операции транзакиции
    """
    for dct in transact:
        yield dct['description']


def split_card(num: int) -> str:
    """
    Дополнительная функция к card_number_generator(). Присваивает номер карте, разделяет его по четыре цифры
    :param num: номер карты
    :return: номер карты, разделенный по четыре цифры
    """
    card = '0' * (16 - len(str(num))) + str(num)
    return ' '.join([card[(4 * i):(4 * i + 4)] for i in range(4)])


def card_number_generator(start: int, finish: int) -> Generator:
    """
    Функция генерирует номера карт в заданном диапазоне
    :param start: начальное значение
    :param finish: конечное значение
    :return: генераторное выражение с заданными значениями карт
    """
    if start < 0 or finish < 0 or finish > 9999_9999_9999_9999:
        raise ValueError('Неверное значение вводных данных')

    cards = (split_card(num) for num in range(start, finish + 1))
    return cards
