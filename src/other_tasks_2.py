from typing import Optional

from src.processing import get_dicts_sorted_by_date


def sorted_by_product_price(product_list: list[dict], product_category: Optional[str] = None) -> list[dict]:
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


def sorted_by_avg_order_list(order_list: list[dict]) -> dict[dict]:
    """
    функция возвращает список словарей,
    содержащий информацию о средней стоимости заказа и количестве заказов за каждый месяц
    :param order_list: {'id': ,'date': ,items': [
                                        {'name': 'товар', 'price': цена, 'quantity': количество},
                                        {}
    :return: список словарей усредненных цен за товары по месяцам
    """
    monthly_statistics = {}

    for order in order_list:
        order_date = order['date']
        year_month = order_date[:7]

        total_order_cost = 0
        for item in order['items']:
            total_order_cost += item['price'] * item['quantity']

        if year_month in monthly_statistics:
            monthly_statistics[year_month]['total_cost'] += total_order_cost
            monthly_statistics[year_month]['order_count'] += 1
        else:
            monthly_statistics[year_month] = {'total_cost': total_order_cost, 'order_count': 1}

    result = {}
    for year_month, stats in monthly_statistics.items():
        average_order_value = stats['total_cost'] / stats['order_count']
        result[year_month] = {
            'average_order_value': average_order_value,
            'order_count': stats['order_count']
        }

    return result
