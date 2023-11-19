from src.logger_ import setup_logging
from src.utils import transaction_amount_rub, currency_from_api_rub_rate, transactions_json_to_dict
from dotenv import load_dotenv
import os
from src.masks import card_mask, account_mask

load_dotenv()
API_KEY = os.environ.get('API_KEY')
logger = setup_logging()


def main():
    logger.info("Application starts....")
    transactions_json_to_dict('operations.json')
    rub_usd_rate = currency_from_api_rub_rate('USD')
    transaction_amount_rub({
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560"
    }, rub_usd_rate)

    transaction_amount_rub({
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amunt": "8221.37",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560"
    }, rub_usd_rate)

    transaction_amount_rub({
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }, rub_usd_rate)

    account_mask('35383033374447895560')
    card_mask('7158300734726758')
    account_mask('3538303374447895560')
    card_mask('715830073476758')
    logger.info("Application finished....")


if __name__ == '__main__':
    main()
