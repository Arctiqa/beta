# from src.widget import registration_date

dic_list = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]


def get_dicts_not_executed(dict_list: list[dict], state: str = 'EXECUTED') -> list[dict]:
    new_list = []
    for dict_ in dict_list:
        if dict_['state'] == state:
            new_list.append(dict_)
    return new_list


def get_dicts_sorted_by_date(dict_list: list[dict], sort_type: bool = True) -> list[dict]:
    new_list = sorted(dict_list, key=lambda dict_: dict_['date'], reverse=sort_type)
    return new_list


print(dic_list)
print()
print(get_dicts_sorted_by_date(dic_list))
print(get_dicts_sorted_by_date(dic_list, False))
print(get_dicts_not_executed(dic_list, 'CANCELED'))
print(get_dicts_not_executed(dic_list))
