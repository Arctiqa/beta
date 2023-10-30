from src.processing import get_dicts_sorted_by_date, get_dicts_not_executed
from src.other_tasks_2 import sorted_by_avg_order_list, sorted_by_product_price


orders = [
    {
        'id': 1,
        'date': '2023-01-15',
        'items': [
            {'name': 'Product A', 'price': 10, 'quantity': 2},
            {'name': 'Product B', 'price': 20, 'quantity': 1}
        ]
    },
    {
        'id': 2,
        'date': '2023-01-20',
        'items': [
            {'name': 'Product A', 'price': 10, 'quantity': 1},
            {'name': 'Product C', 'price': 15, 'quantity': 3}
        ]
    },
    {
        'id': 3,
        'date': '2023-02-10',
        'items': [
            {'name': 'Product B', 'price': 20, 'quantity': 1}
        ]
    },
]


main_task_input = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                   {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                   {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                   {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

dop_task_1 = [{'name': 'qer', 'price': 230, 'category': 'potato1'},
              {'name': 'sdf', 'price': 50, 'category': 'potato2'},
              {'name': 'qvsr', 'price': 2430, 'category': 'potato3'},
              {'name': 'qdsr', 'price': 630, 'category': 'potato4'},
              {'name': 'qer', 'price': 235, 'category': 'potato1'}]

dop_task_2 = [{
    'id': 1,
    'date': '2023-10-30T02:26:18.671407',
    'items': [
        {'name': 'Товар 1', 'price': 100, 'quantity': 2},
        {'name': 'Товар 2', 'price': 50, 'quantity': 1},
        {'name': 'Товар 3', 'price': 200, 'quantity': 3}
    ]
},

    {
        'id': 2,
        'date': '2023-10-31T02:26:18.671407',
        'items': [
            {'name': 'Товар 4', 'price': 150, 'quantity': 1},
            {'name': 'Товар 2', 'price': 50, 'quantity': 2},
            {'name': 'Товар 5', 'price': 300, 'quantity': 1}
        ]
    },

    {
        'id': 3,
        'date': '2023-11-01T02:26:18.671407',
        'items': [
            {'name': 'Товар 1', 'price': 100, 'quantity': 1},
            {'name': 'Товар 3', 'price': 200, 'quantity': 2},
            {'name': 'Товар 6', 'price': 120, 'quantity': 3}
        ]
    },

    {
        'id': 4,
        'date': '2023-11-02T02:26:18.671407',
        'items': [
            {'name': 'Товар 2', 'price': 50, 'quantity': 3},
            {'name': 'Товар 4', 'price': 150, 'quantity': 2}
        ]
    },

    {
        'id': 5,
        'date': '2023-11-03T02:26:18.671407',
        'items': [
            {'name': 'Товар 5', 'price': 300, 'quantity': 1},
            {'name': 'Товар 1', 'price': 100, 'quantity': 4},
            {'name': 'Товар 3', 'price': 200, 'quantity': 2}
        ]
    }]


print(main_task_input)
print()
print(get_dicts_sorted_by_date(main_task_input))
print(get_dicts_sorted_by_date(main_task_input, False))
print(get_dicts_not_executed(main_task_input, 'CANCELED'))
print(get_dicts_not_executed(main_task_input))
print('---------------')
print(sorted_by_product_price(dop_task_1))
print(sorted_by_product_price(dop_task_1, 'potato1'))
print(sorted_by_avg_order_list(dop_task_2))
print(sorted_by_avg_order_list(orders))
