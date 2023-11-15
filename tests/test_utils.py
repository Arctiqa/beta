import os
import json
from unittest.mock import patch
import pytest
from src.utils import transaction_amount_rub, transactions_json_to_dict, usd_to_rub_rate
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY')
print(os.getcwd())


@pytest.fixture
def test_dict():
    file_path = os.path.join(os.path.dirname(__file__), '../data/operations.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_transactions_json_to_dict(test_dict):
    json_file = 'operations.json'
    result = transactions_json_to_dict(json_file)
    assert result == test_dict


def test_transactions_json_to_dict_not_found(capsys):
    json_file = 'not_exist.json'
    result = transactions_json_to_dict(json_file)
    log_message = capsys.readouterr()

    assert result is None
    assert f'File {json_file} not found.' == log_message.out.strip()


def test_transactions_json_to_dict_invalid_json(capsys):
    json_file = 'invalid_json.json'
    result = transactions_json_to_dict(json_file)
    log_message = capsys.readouterr()

    assert result is None
    assert "Invalid JSON data." == log_message.out.strip()


def test_usd_to_rub_rate():
    with patch('requests.request') as mock_get:
        mock_get.return_value.json.return_value = {'base': 'USD', 'rates': {'RUB': 90.0}}
        assert usd_to_rub_rate('USD') == 90.0
        mock_get.assert_called_once_with("GET",
                                         "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD",
                                         headers={"apikey": API_KEY})

    with patch('requests.request') as mock_get_none:
        mock_get_none.return_value.json.return_value = None
        assert usd_to_rub_rate('USD') is None
        mock_get_none.assert_called_once_with(
            "GET",
            "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD",
            headers={"apikey": API_KEY}
        )


def test_transaction_amount_rub():
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
