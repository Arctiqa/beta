g = ['hello', 'world', 'apple', 'pear', 'banana', 'pop']
h = ['', 'madam', 'racecar', 'noon', 'level', '']
k = [2, 3, 5, 7, 11]
b = [-5, -7, -9, -13]


def matching_letters(wordlist: list) -> list:
    tenet_list = []
    for word in wordlist:
        if word == '':
            continue
        elif word[0] == word[-1]:
            tenet_list.append(word)
    return tenet_list


def max_nums_multiplication(num_list: list) -> list:
    sorted_list = sorted(num_list)
    value1 = sorted_list[-1] * sorted_list[-2]
    value2 = sorted_list[0] * sorted_list[1]
    return max(value1, value2)


print(matching_letters(g))
print(matching_letters(h))

print(max_nums_multiplication(k))
print(max_nums_multiplication(b))


