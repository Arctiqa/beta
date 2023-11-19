import os
import json
from unittest.mock import patch
import pytest
from src.utils import transaction_amount_rub, transactions_json_to_dict, currency_from_api_rub_rate
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


def test_currency_from_api_rub_rate(caplog):
    with patch('requests.request') as mock_get:
        mock_get.return_value.json.return_value = {'base': 'USD', 'rates': {'RUB': 90.0}}
        assert currency_from_api_rub_rate('USD', API_KEY) == 90.0
        mock_get.assert_called_once_with("GET",
                                         "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD",
                                         headers={"apikey": API_KEY})
        with caplog.at_level(logging.INFO):
            currency_from_api_rub_rate('USD')
            assert 'response value has been received from API' in caplog.text

    with patch('requests.request') as mock_get_none:
        mock_get_none.return_value.json.return_value = None
        assert currency_from_api_rub_rate('USD') is None
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

    assert transaction_amount_rub(rub_transaction, 91.3) == 31957.58
    assert round(transaction_amount_rub(usd_transaction, 100.0), 1) == 822137.0
    assert transaction_amount_rub(incorrect_transaction, 92.4) is None

    with caplog.at_level(logging.INFO):
        transaction_amount_rub(rub_transaction, 91.3)
        (transaction_amount_rub(usd_transaction, 100.0), 1)
        transaction_amount_rub(incorrect_transaction, 92.4)

        assert 'transaction has been completed, currency - RUB, id - 441945886' in caplog.text
        assert 'transaction has been completed, currency - USD, id - 41428829' in caplog.text
        assert "key 'operationAmount' not found in transaction." in caplog.text
