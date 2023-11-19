import json
import os
import requests
import logging
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY')
logger = logging.getLogger(__name__)


def currency_to_rub_rate(currency: str) -> Optional[float]:
    """
    Запрашивает курс валюты от API и возвращает значение курса RUB к USD
    :param currency: запрашиваемая валюта
    :return: курс рубля по отношению к запрашиваемой валюте
    """
    if API_KEY is None:
        logger.error('API is not defined')
        raise Exception('API не определен')
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    try:
        response = requests.request("GET", url, headers={"apikey": API_KEY}).json()
        return float(response['rates']['RUB'])
    except Exception as e:
        logger.error(f'Error during API request: {e}')
        return None


def transactions_json_to_dict(json_file: str) -> Any:
    """
    Функция принимает json файл с транзакциями, возвращает отредактированный json файл в формате python
    :param json_file: файл с транзакциями в формате json
    :return: отредактированный файл json
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', json_file), 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f'json file {os.path.join(os.getcwd(), "data", json_file)}'
                        f' converted to python format')
            return data

    except json.JSONDecodeError:
        logger.warning("Invalid JSON data.")
        print("Invalid JSON data.")
        return []
    except FileNotFoundError:
        logger.warning(f"File {json_file} not found.")
        print(f"File {json_file} not found.")
        return []


def transaction_amount_rub(transaction: dict[str, dict], currency_rate: float) -> Optional[float]:
    """
    Принимает на вход транзакцию, выводит сумму транзакции в рублях
    :param transaction: транзакция в виде словаря
    :param currency_rate : курс рубля по отношению к валюте currency_rate
    :return float: сумма транзакции в рублях
    """
    try:
        if transaction["operationAmount"]['currency']['code'] == 'RUB':
            logger.info(f'transaction has been completed, currency - RUB, id - {transaction["id"]}')
            return float(transaction["operationAmount"]["amount"])
        else:
            usd_rub_amount = float(transaction["operationAmount"]['amount'])
            result_rub = usd_rub_amount * currency_rate
            logger.info(f'transaction has been completed, currency - '
                        f'{(transaction["operationAmount"]["currency"]["code"])}, id - {transaction["id"]}')
            return float(result_rub)
    except KeyError as e:
        print(f"Key {str(e)} not found in transaction.")
        logger.error(f"key {str(e)} not found in transaction.")

        return None
