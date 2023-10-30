from processing import get_dicts_sorted_by_date


def sorted_by_product_dicts(product_list: list[dict], product_category: str = None) -> list[dict]:
    """
    возвращает список словарей, отсортированных по убыванию для продуктов из заданной категории
    :param: список словарей с товарами
    :return: отсортированный по категории список
    """
    if product_category is None:
        new_list = sorted(product_list, key=lambda category: category['price'], reverse=True)
        return new_list
    else:
        new_list = []
        for dict_ in product_list:
            if dict_['category'] == product_category:
                new_list.append(dict_)
        return sorted(new_list, key=lambda category: category['price'], reverse=True)


def sorted_by_avg_order_list(order_list: list[dict]) -> list[dict]:
    """
    функция возвращает список словарей,
    содержащий информацию о средней стоимости заказа и количестве заказов за каждый месяц
    :param order_list: {'id': ,'date': ,items': [
                                        {'name': 'товар', 'price': цена, 'quantity': количество},
                                        {}
    :return:
    """
    sorted_list = get_dicts_sorted_by_date(order_list, False)
    sorted_new_list: list[dict] = []

    for order_month in sorted_list:
        dated = order_month['date'].split('-')[:2]
        price_sum = 0
        quantity_sum = 0
        for item in order_month['items']:
            price_sum += item['price']
            quantity_sum += item['quantity']
        # print(price_sum, quantity_sum)
        changed_items = {'all_price_sum': price_sum, 'all_quantity_sum': quantity_sum}
        list_ = {'date': '-'.join(dated), 'order': changed_items}
        sorted_new_list.append(list_)
    print(sorted_new_list)

    last_date_value = sorted_new_list[0]['date']
    all_price_sum = 0
    all_quantity_sum = 0
    avg_price_list = []

    for order in sorted_new_list:
        if order['date'] == last_date_value:
            all_price_sum += order['order']['all_price_sum']
            all_quantity_sum += order['order']['all_quantity_sum']
            last_date_value = order['date']
        else:
            avg_price_value = all_price_sum / all_quantity_sum
            avg_dict = {'average_order_value': avg_price_value, 'order_count': all_quantity_sum}
            avg_price_list.append(avg_dict)
            all_price_sum = 0
            all_quantity_sum = 0
            all_price_sum += order['order']['all_price_sum']
            all_quantity_sum += order['order']['all_quantity_sum']
            last_date_value = order['date']
    avg_price_value = all_price_sum / all_quantity_sum
    avg_dict = {'average_order_value': avg_price_value, 'order_count': all_quantity_sum}
    avg_price_list.append(avg_dict)
    return avg_price_list



