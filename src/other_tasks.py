import os

g = ['hello', 'world', 'apple', 'pear', 'banana', 'pop']
h = ['', 'madam', 'racecar', 'noon', 'level', '']
k = [2, 3, 5, 7, 11]
b = [-5, -7, -9, -13]
d = [3]


def path_to_directory(path: str = os.getcwd()) -> dict:
    """возвращает путь директории в виде словаря {"files": , "folders": }
    (Перенесено из прошлого урока сюда)"""
    len_dirs = 0
    len_files = 0
    for root, dirs, files in os.walk(path):
        len_dirs += len(dirs)
        len_files += len(files)
    return {"files": len_files, "folders": len_dirs}


def matching_letters(wordlist: list[str]) -> list[str]:
    """
    :param: список слов
    :return: список слов, если первая и последняя буква совпадают
    """
    tenet_list = []
    for word in wordlist:
        if word == '':
            continue
        elif word[0] == word[-1]:
            tenet_list.append(word)
    return tenet_list


def max_nums_multiplication(num_list: list[int]) -> int:
    """
    :param: список из цифр
    :return: максимально возможное произведение двух чисел из списка
    """
    if len(num_list) < 2:
        return 0
    else:
        sorted_list = sorted(num_list)
        value1 = sorted_list[-1] * sorted_list[-2]
        value2 = sorted_list[0] * sorted_list[1]
        return max(value1, value2)


print(path_to_directory())
print()
print(matching_letters(g))
print(matching_letters(h))
print()
print(max_nums_multiplication(k))
print(max_nums_multiplication(b))
print(max_nums_multiplication(d))
