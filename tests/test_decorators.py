from datetime import datetime, timedelta

import pytest

from src.decorators import my_function


@pytest.fixture
def log_file():
    return "mylog.txt"


def test_my_function():
    result = my_function(3, 5)
    assert result == 8


@pytest.mark.parametrize("args, expected_result", [((1, 2), 3),
                                                   ((3.5, 5), 8.5)])
def test_log(log_file, args, expected_result):
    result = my_function(*args)

    test_time = datetime.now()
    assert result == expected_result

    with open(log_file, "r", encoding="utf-8") as file:
        log_contents = file.readlines()[-1]

    actual_time = datetime.strptime(log_contents[:19], "%Y-%m-%d %H:%M:%S")

    assert test_time - actual_time < timedelta(seconds=1)
    assert f"{my_function.__name__}, ok" in log_contents


@pytest.mark.parametrize("args, expected_result",
                         [((1, 't'), 'error: Ошибка типа данных'),
                          (('r', 't'), 'error: Ошибка типа данных'),
                          (('r', 4), 'error: Ошибка типа данных')
                          ])
def test_log_errors(log_file, args, expected_result):
    result = my_function(*args)

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert result == expected_result

    with open(log_file, "r", encoding="utf-8") as file:
        log_contents = file.readlines()[-1]

    actual_time = log_contents[:19]

    assert test_time == actual_time
    assert f"{my_function.__name__}, error" in f"{my_function.__name__}, error: Ошибка типа данных" in log_contents
