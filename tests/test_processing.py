import pytest

from src.processing import get_dicts_not_executed, get_dicts_sorted_by_date


@pytest.fixture
def data_list():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]


def test_get_dicts_not_executed(data_list):
    executed_list = get_dicts_not_executed(data_list, state='EXECUTED')
    canceled_list = get_dicts_not_executed(data_list, state='CANCELED')
    state_nothing_list = get_dicts_not_executed(data_list)

    expected_executed_list = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    expected_canceled_list = [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    expected_state_nothing_list = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]

    assert executed_list == expected_executed_list
    assert canceled_list == expected_canceled_list
    assert state_nothing_list == expected_state_nothing_list


def test_get_dicts_sorted_by_date(data_list):
    sorted_by_date = get_dicts_sorted_by_date(data_list, True)
    reverse_sorted_by_date = get_dicts_sorted_by_date(data_list, False)
    sort_type_nothing_by_date = get_dicts_sorted_by_date(data_list)

    expected_sorted_by_date = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                               {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                               {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                               {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    expected_reverse_sorted_by_date = [{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                                       {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                                       {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                                       {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}]
    expected_sort_type_nothing_by_date = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                                          {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                                          {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                                          {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

    assert sorted_by_date == expected_sorted_by_date
    assert reverse_sorted_by_date == expected_reverse_sorted_by_date
    assert sort_type_nothing_by_date == expected_sort_type_nothing_by_date
