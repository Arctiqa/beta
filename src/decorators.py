from datetime import datetime
from functools import wraps
from typing import Any, Callable


def log(filename: Any = None) -> Callable:
    """
    Декоратор проверяет правильный тип входящих в функцию данных int | float
    в случае успеха исполняет функцию, записывает в лог успешное исполнение и время исполнения
    в случае неуспеха выводит в консоль сообщение об ошибке типа данных, записывает в лог время исполнения
    :param filename: название файла, в который записывается результат исполняемого дествия
    :return: возвращает результат функции, либо сообщение об ошибке входных данных
    """
    def wrapper(func: Callable) -> Any:
        @wraps(func)
        def inner(*args: tuple[Any]) -> Any:
            s = tuple(i for i in args if isinstance(i, int | float))
            if args == s:
                result = func(*args)
                log_message = f"{datetime.now()} {func.__name__}, ok"
            else:
                result = "error: Ошибка типа данных"
                log_message = f"{datetime.now()} {func.__name__}," \
                              f" {result}. Inputs: {args}, {func.__name__}"
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(log_message + "\n")
                print(log_message)
            return result

        return inner

    return wrapper


@log(filename="mylog.txt")
def my_function(x: int | float, y: int | float) -> int | float:
    """
    Складывает два числа
    :param x: int | float
    :param y: int | float
    :return: сумма
    """
    return x + y

#
# my_function(1, 2)
# my_function(1, 't')
# my_function('r', 5)
# my_function('r', 't')
