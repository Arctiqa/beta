from src.utils import transaction_amount_rub, usd_to_rub_rate, transactions_json_to_dict
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get('API_KEY')


def main():
    rub_usd_rate = usd_to_rub_rate('USD')
    transactions = transactions_json_to_dict('operations.json')

    for tr in transactions:
        res = transaction_amount_rub(tr, rub_usd_rate)
        print(res)


if __name__ == '__main__':
    main()
