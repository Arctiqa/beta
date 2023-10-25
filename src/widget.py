date = "2018-07-11T02:26:18.671407"
data_input = """
Maestro 1596837868705199
Счет 64686473678894779589
MasterCard 7158300734726758
Счет 35383033474447895560
Visa Classic 6831982476737658
Visa Platinum 8990922113665229
Visa Gold 5999414228426353
Счет 73654108430135874305
"""


def card_information_output(info: str) -> str:
    """
    :param info: счет/номер карты
    :return: маскированный счет входных данных (номера или счета карты)
    """
    info_type = info.split()[0].lower()
    if info_type == 'счет':
        card_account = info
        card_account = card_account.split()[-1]
        return "**" + card_account[-4:]
    else:
        card_number = info
        card_number = card_number.split()[-1]
        if len(card_number) != 16 or not card_number.isdigit():
            return "номер карты должен состоять из шестнадцати цифр"
        else:
            card_number = card_number.replace(card_number[6:12], "******")
            card = []
            for i in range(4):
                card.append(card_number[(4 * i): (4 * i + 4)])
        return " ".join(card)


def registration_date(datetime: str) -> str:
    """
    :param: входящие параметры даты вида "2018-07-11T02:26:18.671407"
    :return: "дата в формате дд.мм.гг
    """
    datet = datetime.split('T')[0].split('-')
    return '.'.join(datet[::-1])


def test(cards_data: str) -> str:
    """тестовая функция"""
    data = cards_data.split('\n')
    output = ''
    for i in data[1:-1]:
        output += card_information_output(i) + '\n'
    return output


print(test(data_input))
print(registration_date(date))
