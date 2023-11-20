from website.models import Inventory

def get_inventory_details():
    inventory_products = Inventory.query.all()
    return inventory_products

def get_inventory_product(sku):
    product = Inventory.query.filter_by(sku=sku).first()
    return product