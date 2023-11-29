'''
Order related function definitions
'''
import logging
from website.models import Order, db, OrderInventoryRelation
from flask_login import current_user
from datetime import datetime

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


def place_order(data):

    try:      
        new_order = Order(
            user_id=current_user.user_id,
            date=datetime.now().strftime("%m %d %Y"),
            units_sold=sum(item['quantity'] for item in data),
            order_status='Placed'  
        )      
        db.session.add(new_order)
        db.session.commit()
     
        for item in data:
            order_inventory_relation = OrderInventoryRelation(
                order_id=new_order.order_id,
                sku=item['sku'],
                quantity=item['quantity']
            )       
            db.session.add(order_inventory_relation)       
        db.session.commit()
        return True

    except Exception as e:      
        db.session.rollback()
        logging.exception(e)
        return False
    
    finally:
        db.session.close()