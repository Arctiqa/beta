from src import masks

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
        return f'Счет {account_masked}'
    else:
        card_number = info_list[-1]
        card_masked = masks.card_mask(card_number)  # src/masks
        info_list[-1] = card_masked
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


def test(cards_data: str) -> str:
    """тестовая функция"""
    data = cards_data.split('\n')
    output = ''
    for i in data[1:-1]:
        output += card_information_output(i) + '\n'
    return output


print(test(data_input))
print(registration_date(date))
