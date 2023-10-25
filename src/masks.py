inp = "Visa Classic 6831982476737658"
acc = "Счет 64686473678894779589"
date = "2018-07-11T02:26:18.671407"


def card_mask(card_number: str) -> str:
    """Функция маскировки номера карты
    :param str card_number: Номер карты
    :return: Маскированный номер
    """
    card_number = card_number.split()[-1]
    if len(card_number) != 16 or not card_number.isdigit():
        return "номер карты должен состоять из шестнадцати цифр"
    else:
        card_number = card_number.replace(card_number[6:12], "******")
        card = []
        for i in range(4):
            card.append(card_number[(4 * i): (4 * i + 4)])
        return " ".join(card)


def account_mask(card_account: str) -> str:
    """Функция маскировки счета
    :param str card_account: Номер счета
    :return: Маскированный счет
    """
    card_account = card_account.split()[-1]
    return "**" + card_account[-4:]


def registration_date(datetime: str) -> str:
    """
    :param: входящие параметры даты вида "2018-07-11T02:26:18.671407"
    :return: "дата в формате дд.мм.гг
    """
    datet = datetime.split('T')[0].split('-')
    return '.'.join(datet[::-1])


print(card_mask(inp))
print(account_mask(acc))
print(registration_date(date))
