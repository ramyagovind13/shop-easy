import logging
from website.models import Order, User

def get_all_orders():
    try:
        orders_list = list()
        orders = Order.query.all()
        for order in orders:
            order_detail = dict()
            user_details = order.user
            order_detail['email'] = user_details.email
            order_detail['name'] = user_details.name
            order_detail['order_id'] = order.order_id
            order_detail['units_sold'] = order.units_sold
            order_detail['date'] = order.format_date()
            order_detail['order_status'] = order.order_status
            orders_list.append(order_detail)
        return orders_list
    except Exception as e:
        logging.exception(e)
        return None
