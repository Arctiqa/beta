from src.logger_ import setup_logging
from src.utils import (transaction_amount_rub, currency_from_api_rub_rate,
                       transactions_json_to_dict, transactions_xlsx_to_dict, transactions_csv_to_dict)
from dotenv import load_dotenv
import os
from unittest.mock import patch

load_dotenv()
API_KEY = os.environ.get('API_KEY')
logger = setup_logging()


def main():
    logger.info("Application starts....")
    j = transactions_json_to_dict('operations.json')
    x = transactions_xlsx_to_dict('transactions_excel.xlsx')
    c = transactions_csv_to_dict('transactions.csv')
    for i in j:
        print(transaction_amount_rub(i, 'USD'))
    print('------------')
    for i in x:
        print(transaction_amount_rub(i, 'EUR'))
    print('------------')
    for i in c:
        print(transaction_amount_rub(i, 'CNY'))
    print('------------')

    currency_from_api_rub_rate('USD', api_key=None)
    with patch('requests.request') as mock_get_none:
        mock_get_none.return_value.json.return_value = None
        currency_from_api_rub_rate("USD", api_key=API_KEY)

    logger.info("Application finished....")


if __name__ == '__main__':
    main()
