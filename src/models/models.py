from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    restaurant_name = db.Column(db.String(150), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='owner')
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    monthly_budget = db.Column(db.Float, default=0.0)
    must_change_password = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def get_restaurant_name(self):
        if self.role == 'owner':
            return self.restaurant_name
        elif self.parent_id:
            parent = User.query.get(self.parent_id)
            return parent.restaurant_name if parent else "N/A"
        return "N/A"

    @property
    def get_restaurant_id(self):
        if self.role == 'owner':
            return self.id
        return self.parent_id

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact_info = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Product', backref='supplier', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    unit = db.Column(db.String(50), nullable=False)
    min_threshold = db.Column(db.Float, nullable=False, default=5.0)
    unit_cost = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=True)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    prep_time = db.Column(db.Integer, nullable=True)
    allergens = db.Column(db.String(250), nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(250), nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class RecipeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity_needed = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product', backref='recipe_items')

class ConsumptionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product')

# ---> FASE 34: TABELLA REGISTRO SPRECHI <---
class WasteLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity_wasted = db.Column(db.Float, nullable=False)
    cost_lost = db.Column(db.Float, nullable=False) 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product')