import os

inp = "8846888895461112"
acc = "88468888954611125896"


def card_mask(card_number: str) -> str:
    """принимает на вход номер карты и возвращает ее маску"""
    if len(card_number) != 16 or not card_number.isdigit():
        return "номер карты должен состоять из шестнадцати цифр"
    else:
        card_number = card_number.replace(card_number[6:12], "******")
        card = []
        for i in range(4):
            card.append(card_number[(4 * i): (4 * i + 4)])
        return " ".join(card)


def account_mask(card_account: str) -> str:
    """принимает на вход номер счёта и возвращает его маску."""
    return "**" + card_account[-4:]


def path_to_directory(path: str = os.getcwd()) -> dict:
    """возвращает путь директории в виде словаря {"files": , "folders": }"""
    len_dirs = 0
    len_files = 0
    for root, dirs, files in os.walk(path):
        len_dirs += len(dirs)
        len_files += len(files)
    return {"files": len_files, "folders": len_dirs}


print(path_to_directory())
print(card_mask(inp))
print(account_mask(acc))
