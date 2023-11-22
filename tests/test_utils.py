import os
import json
from unittest.mock import patch
import pytest
from src.utils import (transaction_amount_rub, transactions_json_to_dict, currency_from_api_rub_rate,
                       transactions_csv_to_dict, transactions_xlsx_to_dict)
from dotenv import load_dotenv
from src.logger_ import setup_logging
import logging

load_dotenv()
API_KEY = os.environ.get('API_KEY')
logger = setup_logging()


@pytest.fixture
def test_dict():
    file_path = os.path.join(os.path.dirname(__file__), '../data/operations.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_transactions_json_to_dict(test_dict, caplog):
    json_file = 'operations.json'
    result = transactions_json_to_dict(json_file)
    assert result == test_dict
    with caplog.at_level(logging.INFO):
        transactions_json_to_dict(json_file)
    assert f'json file {os.path.join(os.getcwd(), "data", json_file)} converted to python format' in caplog.text


def test_transactions_json_to_dict_not_found(caplog):
    json_file = 'not_exist.json'
    result = transactions_json_to_dict(json_file)

    assert result == []
    assert f"File {json_file} not found." in caplog.text


def test_transactions_json_to_dict_invalid_json(caplog):
    json_file = 'invalid_json.json'
    result = transactions_json_to_dict(json_file)

    assert result == []
    assert "Invalid JSON data." in caplog.text


def test_currency_from_api_rub_rate_none(caplog):
    with patch('requests.request') as mock_get_none:
        mock_get_none.return_value.json.return_value = None
        assert currency_from_api_rub_rate('USD', API_KEY) is None
        mock_get_none.assert_called_once_with(
            "GET",
            "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD",
            headers={"apikey": API_KEY})
        with caplog.at_level(logging.INFO):
            currency_from_api_rub_rate('USD', API_KEY)
            assert "Error during API request: 'NoneType' object is not subscriptable" in caplog.text

    currency_from_api_rub_rate('USD', api_key=None)
    assert 'Error during API request: API не определен' in caplog.text


def test_transaction_amount_rub(caplog):
    rub_transaction = {
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
    }

    usd_transaction = {
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
    }
    incorrect_transaction = {}

    with patch('src.utils.currency_from_api_rub_rate') as mock_currency:
        mock_currency.return_value = 100.0
        with caplog.at_level(logging.INFO):
            transaction_amount_rub(usd_transaction, 'USD')
            assert 'transaction has been completed, currency - USD, id - 41428829' in caplog.text
        result = transaction_amount_rub(usd_transaction, "USD")
    assert result == 'Transaction id - 41428829, USD to RUB - 822137.0000000001'

    assert transaction_amount_rub(incorrect_transaction, 'USD') is None
    assert transaction_amount_rub(rub_transaction, 'USD') == 'Transaction id - 441945886, RUB - 31957.58'

    with caplog.at_level(logging.INFO):
        transaction_amount_rub(rub_transaction, 'USD')
        transaction_amount_rub(incorrect_transaction, 'USD')

        assert 'transaction has been completed, currency - RUB, id - 441945886' in caplog.text
        assert "key 'operationAmount' not found in transaction." in caplog.text


def test_transactions_xlsx_to_dict(caplog):
    data_file = 'transactions_excel.xlsx'
    result = transactions_xlsx_to_dict(data_file)
    sample = {
        'id': 650703.0,
        'state': 'EXECUTED',
        'date': '2023-09-05T11:30:32Z',
        'from': 'Счет 58803664561298323391',
        'to': 'Счет 39745660563456619397',
        'description': 'Перевод организации',
        'operationAmount': {
            'amount': 16210.0,
            'currency': {
                'name': 'Sol',
                'code': 'PEN'
            }
        }
    }
    assert result[0] == sample
    with caplog.at_level(logging.INFO):
        transactions_xlsx_to_dict(data_file)
        assert f'xlsx file {os.path.join(os.getcwd(), "data", data_file)} converted to python format' in caplog.text

    data_file = 'transaction_excel_empty.csv'
    result = transactions_xlsx_to_dict(data_file)
    assert result == []

    data_file = 'transaction_excel_invalid.csv'
    result = transactions_xlsx_to_dict(data_file)
    assert result == []

    data_file = 'not_exist.csv'
    result = transactions_xlsx_to_dict(data_file)
    assert result == []


def test_transactions_csv_to_dict(caplog):
    data_file = 'transactions.csv'
    result = transactions_csv_to_dict(data_file)
    sample = {
        'id': 650703.0,
        'state': 'EXECUTED',
        'date': '2023-09-05T11:30:32Z',
        'from': 'Счет 58803664561298323391',
        'to': 'Счет 39745660563456619397',
        'description': 'Перевод организации',
        'operationAmount': {
            'amount': 16210.0,
            'currency': {
                'name': 'Sol',
                'code': 'PEN'
            }
        }
    }
    assert result[0] == sample
    with caplog.at_level(logging.INFO):
        transactions_csv_to_dict(data_file)
        assert f'csv file {os.path.join(os.getcwd(), "data", data_file)} converted to python format' in caplog.text

    data_file = 'transaction_empty.csv'
    result = transactions_csv_to_dict(data_file)
    assert result == []

    data_file = 'transaction_invalid.csv'
    result = transactions_csv_to_dict(data_file)
    assert result == []

    data_file = 'not_exsist.csv'
    result = transactions_csv_to_dict(data_file)
    assert result == []
