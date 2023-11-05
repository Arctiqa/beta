import pytest

from src.generators import (filter_by_currency, card_number_generator,
                            transaction_descriptions, split_card)


@pytest.fixture()
def transact_list():
    tranc = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
    return tranc


@pytest.mark.parametrize('currency, expected', [('USD', [939719570, 142264268]),
                                                ('RUB', [873106923, 594226727])])
def test_filter_by_currency(transact_list, currency, expected):
    usd_transactions = filter_by_currency(transact_list, currency)
    rub_transactions = filter_by_currency(transact_list, currency)

    for i in range(2):
        assert next(usd_transactions)["id"] == expected[i]
    for i in range(2):
        assert next(rub_transactions)["id"] == expected[i]


@pytest.mark.parametrize('expected', [(['Перевод организации',
                                        'Перевод со счета на счет',
                                        'Перевод со счета на счет',
                                        'Перевод с карты на карту',
                                        'Перевод организации'])])
def test_transaction_descriptions(transact_list, expected):
    descriptions = transaction_descriptions(transact_list)
    assert list(descriptions) == expected


@pytest.mark.parametrize('num, expected', [(101, '0000 0000 0000 0101'),
                                           (20515, '0000 0000 0002 0515'),
                                           (9999999999988001, '9999 9999 9998 8001')])
def test_split_card(num, expected):
    assert split_card(num) == expected


@pytest.mark.parametrize('start, finish, expected', [(101, 105, ['0000 0000 0000 0101',
                                                                 '0000 0000 0000 0102',
                                                                 '0000 0000 0000 0103',
                                                                 '0000 0000 0000 0104',
                                                                 '0000 0000 0000 0105']),
                                                     (10_0705, 10_0708, ['0000 0000 0010 0705',
                                                                         '0000 0000 0010 0706',
                                                                         '0000 0000 0010 0707',
                                                                         '0000 0000 0010 0708'])
                                                     ])
def test_card_number_generator(start, finish, expected):
    result = list(card_number_generator(start, finish))
    assert result == expected


@pytest.mark.parametrize('start, finish', [(-1, 100),
                                           (3, -7),
                                           (9999_9999_9999_9998, 1_0000_0000_0000_0000)])
def test_card_number_generator_invalid_value(start, finish):
    with pytest.raises(ValueError):
        card_number_generator(start, finish)
