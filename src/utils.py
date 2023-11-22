import json
import os
import requests
import logging
from typing import Optional, Any, Callable
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.environ.get('API_KEY')
logger = logging.getLogger(__name__)


def currency_value_cache(func: Callable) -> Any:
    """
    Декоратор сохраняет значение валюты по отношению к рублю в кэш
    :param func: src.utils.currency_from_api_rub_rate
    :return: значение валюты по отношению к рублю
    """
    cache: dict = {}

    def wrapper(currency: str, api_key: str) -> Any:
        try:
            if api_key is None:
                raise ValueError('API не определен')
            if currency in cache:
                logger.info('response value has been received from API cache')
                return cache[currency]
            else:
                result = func(currency, api_key)
                if not None:
                    cache[currency] = result
                    logger.info('response value has been received from API')
                else:
                    raise ValueError('API не определен')
            return result
        except Exception as e:
            logger.error(f'Error during API request: {e}')
            return None

    return wrapper


@currency_value_cache
def currency_from_api_rub_rate(currency: str, api_key: Optional[str] = API_KEY) -> Optional[float]:
    """
    Запрашивает курс валюты от API и возвращает значение курса RUB к USD
    :param currency: запрашиваемая валюта
    :param api_key: API_KEY
    :return: курс рубля по отношению к запрашиваемой валюте
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    try:
        if api_key is None:
            raise ValueError('API не определен')
        response = requests.request("GET", url, headers={"apikey": api_key}).json()
        logger.info('response value has been received from API')
        return float(response['rates']['RUB'])
    except Exception as e:
        logger.error(f'Error during API request: {e}')
        return None


def transactions_json_to_dict(json_file: str) -> Any:
    """
    Функция принимает json файл с транзакциями, возвращает отредактированный файл в виде списка словарей
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
        return []
    except FileNotFoundError:
        logger.warning(f"File {json_file} not found.")
        return []


def transactions_csv_to_dict(data_file: str) -> Any:
    """
    Функция принимает csv файл с транзакциями, возвращает отредактированный файл в виде списка словарей
    :param data_file: файл с транзакциями в формате csv
    :return: отредактированный файл csv
    """
    path = f'{os.path.join(os.path.dirname(__file__), "..", "data", data_file)}'
    try:
        data_dict = pd.read_csv(path, sep=';').to_dict(orient='records')
        for i in data_dict:
            i["operationAmount"] = {
                'amount': i['amount'],
                'currency': {
                    'name': i['currency_name'],
                    'code': i['currency_code']
                }
            }
            del i['amount'], i['currency_name'], i['currency_code']
        logger.info(f'csv file {os.path.join(os.getcwd(), "data", data_file)}'
                    f' converted to python format')
        return data_dict
    except pd.errors.EmptyDataError:
        logging.error("Invalid csv file.")
        return []
    except FileNotFoundError:
        logger.warning(f"File {data_file} not found.")
        return []


def transactions_xlsx_to_dict(data_file: str) -> Any:
    """
    Функция принимает excel файл с транзакциями, возвращает отредактированный файл в виде списка словарей
    :param data_file: файл с транзакциями в формате excel
    :return: отредактированный файл excel
    """
    path = f'{os.path.join(os.path.dirname(__file__), "..", "data", data_file)}'
    try:
        data = pd.read_excel(path)
        data_dict = data.to_dict(orient='records')
        for i in data_dict:
            i["operationAmount"] = {
                'amount': i['amount'],
                'currency': {
                    'name': i['currency_name'],
                    'code': i['currency_code']
                }
            }
            del i['amount'], i['currency_name'], i['currency_code']
        logger.info(f'xlsx file {os.path.join(os.getcwd(), "data", data_file)}'
                    f' converted to python format')
        return data_dict
    except pd.errors.EmptyDataError:
        logger.warning("Invalid csv file.")
        return []
    except FileNotFoundError:
        logger.warning(f"File {data_file} not found.")
        return []


def transaction_amount_rub(transaction: dict[str, dict], currency: str) -> Optional[str]:
    """
    Принимает на вход транзакцию, выводит сумму транзакции в рублях
    :param transaction: транзакция в виде словаря
    :param currency : конвертируемая валюта к курсу рубля
    :return float: сумма транзакции в рублях
    """
    try:
        if transaction["operationAmount"]['currency']['code'] == 'RUB':
            logger.info(f'transaction has been completed, currency - RUB, id - {transaction["id"]}')
            return f"Transaction id - {transaction['id']}, " \
                   f"RUB - {float(transaction['operationAmount']['amount'])}"
        elif transaction["operationAmount"]['currency']['code'] == currency:
            value_rate = currency_from_api_rub_rate(currency, API_KEY)
            usd_rub_amount = float(transaction["operationAmount"]['amount'])
            if not value_rate:
                logger.error('transaction has been completed with error')
                return None
            else:
                result_rub = usd_rub_amount * value_rate
                logger.info(f'transaction has been completed, currency - '
                            f'{(transaction["operationAmount"]["currency"]["code"])}, id - {transaction["id"]}')
                return f"Transaction id - {transaction['id']}, " \
                       f"{transaction['operationAmount']['currency']['code']} to RUB - {float(result_rub)}"
        else:
            return f"Операция совершена не в {currency}"

    except KeyError as e:
        logger.error(f"key {str(e)} not found in transaction.")

        return None
