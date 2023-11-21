'''
Order related function definitions
'''

def get_order_details(current_user):
    user_orders = current_user.orders
    return user_orders

def get_ordered_products(order_details):
    orders = list()
    for order in order_details:
        products = dict()
        products['order'] = order
        products['items'] = list()
        product_details = order.inventory
        for product in product_details:
            unit = dict()
            unit['name'] = product.name
            products['items'].append(unit)
        orders.append(products)
    return orders