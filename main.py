from src.logger_ import setup_logging
from src.utils import (transaction_amount_rub, currency_from_api_rub_rate,
                       transactions_json_to_dict, transactions_xlsx_to_dict, transactions_csv_to_dict)
from src.processing import (get_dicts_sorted_by_date, searching_description,
                            dict_counter_by_description, get_dicts_not_executed)
from src.widget import registration_date, card_information_output
from src.generators import filter_by_currency, transaction_descriptions
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get('API_KEY')
logger = setup_logging()


def main():
    sorted_lst = []
    user_description_key = ''
    existing_transactions = []
    user_input = ''
    unique_descriptions_count = []

    while user_input != 'EXIT':
        print("""Привет! Добро пожаловать в программу работы с банковскими транзакициями.
    Выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из json файла
    2. Получить информацию о транзакциях из csv файла
    3. Получить информацию о транзакциях из xlsx файла""")
        user_input = input(':')
        if user_input == '1':
            print('Для обработки выбран json файл.')
            file_ = transactions_json_to_dict('operations.json')
        elif user_input == '2':
            print('Для обработки выбран csv файл.')
            file_ = transactions_csv_to_dict('transactions.csv')
        elif user_input == '3':
            print('Для обработки выбран xlsx файл.')
            file_ = transactions_xlsx_to_dict('transactions_excel.xlsx')
        else:
            continue
        print("""Введите статус по которому необходимо выполнить фильтрацию.
    Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""")
        user_input = input(':').upper()
        while user_input not in ['EXECUTED', 'CANCELED', 'PENDING']:
            print(f'Статус операции {user_input} недоступен.')
            print("""Введите статус по которому необходимо выполнить фильтрацию.
    Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""")
            user_input = input(':').upper()

        sorted_by_state = get_dicts_not_executed(file_, state=user_input)

        print("Программа: Отсортировать операции по дате? Да/Нет")
        while user_input not in ['да', 'нет']:
            user_input = input(':').lower()
            if user_input in ['да', 'y']:
                print('Отсортировать по возрастанию или по убыванию? Да/Нет')
                user_input = input(':').lower()

                if user_input in ['да', 'y']:
                    sorted_lst = get_dicts_sorted_by_date(sorted_by_state, sort_type=False)
                    break
                elif user_input in ['нет', 'n']:
                    sorted_lst = get_dicts_sorted_by_date(sorted_by_state, sort_type=True)
                    break
            elif user_input in ['нет', 'n']:
                sorted_lst = sorted_by_state
                break
        flag = True
        while flag:
            print('Произведенные в какой валюте транзакции вы хотите вывести')
            user_currency_key = input(':').upper()
            print('Отфильтровать список транзакций по определенному слову в описании? Да/Нет')
            user_input = input(':').lower()

            if user_input in ['да', 'y']:
                print('Введите ключевое слово')
                user_description_key = input(':').lower()

            currency_filtered_trs = list(filter_by_currency(sorted_lst, user_currency_key))
            description_filtered_trs = searching_description(currency_filtered_trs, search_str=user_description_key)

            unique_descriptions = list(set(transaction_descriptions(description_filtered_trs)))

            unique_descriptions_dct = {key: 0 for key in unique_descriptions}

            print('Распечатываю итоговый список транзакций...')
            value = currency_from_api_rub_rate(user_currency_key, API_KEY)

            if value is None:
                print('Не удалось завершить операцию. '
                      'Пожалуйста, проверьте правильность указанного кода валюты.')
                continue
            else:
                description_count_dict = dict_counter_by_description(description_filtered_trs, unique_descriptions_dct)
                for key, value in description_count_dict.items():
                    unique_descriptions_count.append(f'{key} - {value}\n')
                for dct in description_filtered_trs:
                    tr_amount = transaction_amount_rub(dct, user_currency_key)
                    date = registration_date(dct.get('date'))
                    description = dct.get('description')
                    from_ = card_information_output(dct.get('from'))
                    to = card_information_output(dct.get('to'))

                    transactions_info = f"""{date} {description}
{from_} -> {to}
Сумма: {tr_amount}\n
"""
                    existing_transactions.append(transactions_info)
                flag = False
        if len(existing_transactions) > 0:
            print(*existing_transactions)
            print(f'Всего транзакций найдено: {len(existing_transactions)}\n')
            print(f'{"".join(unique_descriptions_count)}\n\n')
            unique_descriptions_count.clear()
            existing_transactions.clear()
        else:
            print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации\n\n')
            unique_descriptions_count.clear()
            existing_transactions.clear()


if __name__ == '__main__':
    main()
