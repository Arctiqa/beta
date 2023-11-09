from datetime import datetime
from functools import wraps
from typing import Any, Callable


def log(filename: Any = None) -> Callable:
    """
    Декоратор записывает в лог данные об исполняемой функции и время исполнения функции
    в случае успеха исполняет функцию, записывает в лог успешное исполнение и время исполнения
    в случае неуспеха выводит в консоль сообщение об ошибке, записывает в лог ошибку время исполнения
    :param filename: название логфайла, в который записывается результат исполняемого дествия
    :return: возвращает результат исполнения функции, либо сообщение об ошибке
    """

    def wrapper(func: Callable) -> Any:
        @wraps(func)
        def inner(*args: tuple[int | float]) -> Any:
            try:
                result = func(*args)
                log_message = f"{datetime.now()} {func.__name__}, ok"
            except Exception as e:
                result = str(e)
                log_message = f"{datetime.now()} {func.__name__}," \
                              f" error:{result}. Inputs: {args}, {func.__name__}"
            if filename is None:
                print(log_message)
            else:
                with open(filename, 'a', encoding='utf-8') as file:
                    file.write(log_message + "\n")

            return result

        return inner

    return wrapper


@log(filename="mylog.txt")
def my_function(x: Any, y: Any) -> Any:
    """
    Складывает два значения
    :param x: x
    :param y: y
    :return: сумма
    """
    return x + y

#
# my_function(1, 2)
# my_function(1, 't')
# my_function('r', 5)
# my_function('r', 't')
