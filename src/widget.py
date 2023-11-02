from src import masks


def card_information_output(info: str) -> str:
    """
    Функция определяет тип поступающей информации (счет или карта),
    возвращая маскированный формат
    :param info: счет/номер карты
    :return: маскированный счет входных данных (номер или счет карты)
    """
    info_list = info.split()
    info_type = info_list[0]
    if info_type == 'Счет':
        card_account = info
        card_account = card_account.split()[-1]
        account_masked = masks.account_mask(card_account)  # src/masks
        if len(account_masked) != 6:
            return account_masked
        else:
            return f'Счет {account_masked}'

    else:
        card_number = info_list[-1]
        card_masked = masks.card_mask(card_number)  # src/masks
        info_list[-1] = card_masked
        if card_masked.replace(' ', '').isalpha():
            return card_masked
        else:
            return " ".join(info_list)


def registration_date(datetime: str) -> str:
    """
    На вход подается строка в формате: дата, время и номер "транзакции?",
    функция возвращает дату в нужном формате
    :param: входящие параметры даты вида "2018-07-11T02:26:18.671407"
    :return: "дата в формате дд.мм.гг
    """
    datet = datetime.split('T')[0].split('-')
    return '.'.join(datet[::-1])
