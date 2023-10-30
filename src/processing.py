def get_dicts_not_executed(dict_list: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    возвращает список словарей, отсортированных по значению state
    :param dict_list: [{'id': 'идентификатор', 'state': 'состояние', 'date': 'дата'}]
    :param state: состояние платежа
    :return: отсортированный список по значению 'state'
    """
    sorted_list = []
    for dict_ in dict_list:
        if dict_['state'] == state:
            sorted_list.append(dict_)
    return sorted_list


def get_dicts_sorted_by_date(dict_list: list[dict], sort_type: bool = True) -> list[dict]:
    """
    возвращает отсортированый по убыванию/возрастанию даты список словарей
    :param dict_list: [{'id': 'идентификатор', 'state': 'состояние', 'date': 'дата'}]
    :param sort_type: возрастание/убывание
    :return: отсортированный список по значению 'date'
    """
    new_list = sorted(dict_list, key=lambda dict_: dict_['date'], reverse=sort_type)
    return new_list
