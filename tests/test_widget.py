import pytest
from src.widget import card_information_output, registration_date


@pytest.mark.parametrize("data, expected_result", [('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
                                                   ('Счет 35383033474447895560', 'Счет **5560'),
                                                   ('Visa Classic 6831982477658',
                                                    'номер карты должен состоять из шестнадцати цифр'),
                                                   ('Счет 736541084301358743054566',
                                                    'номер счета должен состоять из двадцати цифр')])
def test_card_information_output(data, expected_result):
    assert card_information_output(data) == expected_result


def test_registration_date():
    assert registration_date("2018-07-11T02:26:18.671407") == '11.07.2018'
