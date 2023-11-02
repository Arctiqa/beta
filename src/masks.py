def card_mask(card_number: str) -> str:
    """Функция маскировки номера карты
    :param str card_number: Номер карты
    :return: Маскированный номер
    """
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
    if len(card_account) != 20 or not card_account.isdigit():
        return 'номер счета должен состоять из двадцати цифр'
    else:
        return "**" + card_account[-4:]
