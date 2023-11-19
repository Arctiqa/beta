from datetime import datetime, timedelta
import logging
from unittest.mock import patch
from src.utils import currency_from_api_rub_rate
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.environ.get('API_KEY')

test_time = datetime.now()
t = '2023-11-09 00:14:35.210970'
actual_time = datetime.strptime(t[:19], "%Y-%m-%d %H:%M:%S")

dt = test_time - actual_time
time = timedelta(seconds=0.03)
print(dt)
print(time)
print(dt - time)


def capsys(capsys):
    print('stdout')
    log_message = capsys.readouterr()
    assert 'stdout' == log_message.out.strip()


logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s')
console_handler.setFormatter(console_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.warning('Warning message')

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s')
console_handler.setFormatter(console_formatter)
logger.setLevel(logging.DEBUG)
# logger.addHandler(console_handler)
logger.debug('Debug message')

currency_from_api_rub_rate("USD", api_key=None)

with patch('requests.request') as mock_get_none:
    mock_get_none.return_value.json.return_value = None
    currency_from_api_rub_rate("USD", api_key=API_KEY)
