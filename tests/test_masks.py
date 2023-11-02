import pytest
from src.masks import card_mask, account_mask


@pytest.fixture
def test_cards():
    return '7158300734726758'


@pytest.fixture
def test_accounts():
    return '35383033474447895560'


def test_card_mask(test_cards):
    assert card_mask(test_cards) == '7158 30** **** 6758'
    assert card_mask(test_cards[:-1]) == 'номер карты должен состоять из шестнадцати цифр'
    assert card_mask(test_cards + 'letters') == 'номер карты должен состоять из шестнадцати цифр'


def test_account_mask(test_accounts):
    assert account_mask(test_accounts) == '**5560'
    assert account_mask(test_accounts[:-1]) == 'номер счета должен состоять из двадцати цифр'
    assert account_mask(test_accounts + 'letters') == 'номер счета должен состоять из двадцати цифр'
