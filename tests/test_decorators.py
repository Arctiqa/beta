from datetime import datetime, timedelta

import pytest

from src.decorators import my_function, log


@pytest.fixture
def log_file():
    return "mylog.txt"


def test_my_function():
    result1 = my_function(3, 5)
    result2 = my_function(1, 't')
    assert result1 == 8
    assert result2 == "unsupported operand type(s) for +: 'int' and 'str'"


@pytest.mark.parametrize("args, expected_result", [((1, 2), 3),
                                                   ((3.5, 5), 8.5),
                                                   (('r', 't'), 'rt')])  #
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
                         [((1, 't'), "unsupported operand type(s) for +: 'int' and 'str'"),
                          (('r', 4), 'can only concatenate str (not "int") to str')
                          ])
def test_log_errors(log_file, args, expected_result):
    result = my_function(*args)

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert result == expected_result

    with open(log_file, "r", encoding="utf-8") as file:
        log_contents = file.readlines()[-1]

    actual_time = log_contents[:19]

    assert test_time == actual_time
    assert f"{my_function.__name__}, error" in f"{my_function.__name__}, " \
                                               f"error:{result}" in log_contents


@pytest.mark.parametrize("args, expected_result",
                         [((1, 2), 3),
                          ((1, 't'), "unsupported operand type(s) for +: 'int' and 'str'"),
                          (('r', 4), 'can only concatenate str (not "int") to str')
                          ])
def test_filename_is_none(args, expected_result):
    func = log()(my_function)
    result = func(*args)

    assert result == expected_result
