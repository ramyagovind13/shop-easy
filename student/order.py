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
        product_details = order.inventory
        order_product_details = OrderInventoryRelation.query.filter_by(
            order_id=order.order_id).all()

        mapping_dict = {product.sku: product for product in product_details}
        ordered_products = [
            {"name": mapping_dict[product_details.sku].name,
            "quantity": product_details.quantity}
            for product_details in order_product_details
            if product_details.sku in mapping_dict
        ]
        
        products['items'] = ordered_products
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

    except Exception as e:      
        db.session.rollback()
        logging.exception(e)
    
    finally:
        db.session.close()

def cancel_order(order_id):

    try:
        order_to_cancel = Order.query.get(order_id)
        if order_to_cancel:
            order_to_cancel.order_status = "Canceled"
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        logging.exception(e)
        return False

        
