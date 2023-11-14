import json
import os
import requests
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY')


# def get_currency_rate(currency: str) -> float:
#     """Получает курс валюты от API и возвращает его в виде float"""
#
#     url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
#     response = requests.get(url, headers={'apikey': API_KEY})
#     response_data = json.loads(response.text)
#     print(response_data)
#     return response_data
# print(get_currency_rate('USD'))

def usd_to_rub_rate(currency: str) -> Optional[float]:
    """
    Запрашивает курс валюты от API и возвращает значение курса RUB к USD
    :param currency: запрашиваемая валюта
    :return: курс рубля по отношению к запрашиваемой валюте
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.request("GET", url, headers={"apikey": API_KEY}).json()
    print(response)
    if response is None:
        return None
    else:
        return float(response['rates']['RUB'])


def transactions_json_to_dict(json_file: str) -> Any:
    """
    Функция принимает json файл с транзакциями, возвращает отредактированный json файл в формате python
    :param json_file: файл с транзакциями в формате json
    :return: отредактированный файл json
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', json_file), 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    except json.JSONDecodeError:
        print("Invalid JSON data.")
        return None
    except FileNotFoundError:
        print(f"File {json_file} not found.")
        return None


def transaction_amount_rub(transaction: dict[str, dict], currency_rate: float) -> Optional[float]:
    """
    Принимает на вход транзакцию, выводит сумму транзакции в рублях
    :param transaction: транзакция в виде словаря
    :param currency_rate : курс рубля по отношению к валюте currency_rate
    :return float: сумма транзакции в рублях
    """
    try:
        if transaction["operationAmount"]['currency']['code'] == 'RUB':
            return float(transaction["operationAmount"]["amount"])
        else:
            usd_rub_amount = float(transaction["operationAmount"]['amount'])
            result_rub = usd_rub_amount * currency_rate
            return float(result_rub)
    except KeyError as e:
        print(f"Key {str(e)} not found in transaction.")
        return None


f = transactions_json_to_dict('empty_json.json')
print(f)