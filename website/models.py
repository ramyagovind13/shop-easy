'''
Models for shop-easy app
Refer docs/shop-easy-models-ER-diagram to understand 
dependencies and relationships
'''
from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(50))
    name = db.Column(db.String(50))
    
    orders = db.relationship('Order', back_populates='user')
    favorites = db.relationship('Favorite', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')
    carts = db.relationship('Cart', back_populates='user')

    def __repr__(self):
        return f"<User {self.email}>"
     
    def get_id(self):
        return str(self.user_id)

class OrderInventoryRelation(db.Model):
    __tablename__ = 'order_inventory_relation'

    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), primary_key=True)
    sku = db.Column(db.Integer, db.ForeignKey('inventory.sku'), primary_key=True)

class InventoryFavoriteRelation(db.Model):
    __tablename__ = 'inventory_favorite_relation'

    favorite_id = db.Column(db.Integer, db.ForeignKey('favorite.favorite_id'), primary_key=True)
    sku = db.Column(db.Integer, db.ForeignKey('inventory.sku'), primary_key=True)
    
class Inventory(db.Model):
    sku = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(100))
    weight = db.Column(db.Integer)
    expiry_date = db.Column(db.Date)

    orders = db.relationship('Order', secondary='order_inventory_relation', back_populates='inventory')
    favorites = db.relationship('Favorite', secondary='inventory_favorite_relation', back_populates='inventory')
    carts = db.relationship('Cart', secondary='inventory_cart_relation', back_populates='inventory')


    def __init__(self, name, description, quantity, category, weight, expiry_date):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.category = category
        self.weight = weight
        self.expiry_date = expiry_date

    def __repr__(self):
        return f"<Product {self.name}>"

    def format_date(self):
        # Convert the date to "MM/DD/YYYY" format when needed
        return self.expiry_date.strftime("%m/%d/%Y")

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    units_sold = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=func.now())
    order_status = db.Column(db.String(50))

    user = db.relationship('User', back_populates='orders')
    inventory = db.relationship('Inventory', secondary='order_inventory_relation', back_populates='orders')
    
class Favorite(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    user = db.relationship('User', back_populates='favorites')
    inventory = db.relationship('Inventory', secondary='inventory_favorite_relation', back_populates='favorites')

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    suggestion = db.Column(db.Text)

    user = db.relationship('User', back_populates='reviews')

class InvetoryCartRelation(db.Model):
    __tablename__ = 'inventory_cart_relation'

    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'), primary_key=True)
    sku = db.Column(db.Integer, db.ForeignKey('inventory.sku'), primary_key=True)
    quantity = db.Column(db.Integer, default =1)
  
class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    user = db.relationship('User', back_populates='carts')
    inventory = db.relationship('Inventory', secondary='inventory_cart_relation', back_populates='carts')


