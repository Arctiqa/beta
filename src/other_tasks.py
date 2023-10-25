g = ['hello', 'world', 'apple', 'pear', 'banana', 'pop']
h = ['', 'madam', 'racecar', 'noon', 'level', '']
k = [2, 3, 5, 7, 11]
b = [-5, -7, -9, -13]
d = [3]


def matching_letters(wordlist: list[str]) -> list[str]:
    """функция возвращает список слов, если первая и последняя буква совпадают"""
    tenet_list = []
    for word in wordlist:
        if word == '':
            continue
        elif word[0] == word[-1]:
            tenet_list.append(word)
    return tenet_list


def max_nums_multiplication(num_list: list[int]) -> int:
    """функция возвращает максимально возможное произведение двух чисел из списка"""
    if len(num_list) < 2:
        return 0
    else:
        sorted_list = sorted(num_list)
        value1 = sorted_list[-1] * sorted_list[-2]
        value2 = sorted_list[0] * sorted_list[1]
        return max(value1, value2)


print(matching_letters(g))
print(matching_letters(h))

print(max_nums_multiplication(k))
print(max_nums_multiplication(b))
print(max_nums_multiplication(d))
