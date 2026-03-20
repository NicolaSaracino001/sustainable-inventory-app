from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    full_name = db.Column(db.String(150), nullable=False, default="Utente")
    restaurant_name = db.Column(db.String(150), nullable=True) 
    role = db.Column(db.String(20), nullable=False, default='owner') 
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) 
    
    monthly_budget = db.Column(db.Float, nullable=False, default=1000.0)
    
    products = db.relationship('Product', backref='owner', lazy=True, foreign_keys="Product.user_id")
    menu_items = db.relationship('MenuItem', backref='owner', lazy=True, foreign_keys="MenuItem.user_id")
    consumptions = db.relationship('ConsumptionLog', backref='owner', lazy=True, foreign_keys="ConsumptionLog.user_id")
    
    staff_members = db.relationship('User', backref=db.backref('employer', remote_side=[id]))

    @property
    def get_restaurant_id(self):
        return self.parent_id if self.role == 'staff' else self.id
        
    @property
    def get_restaurant_name(self):
        return self.employer.restaurant_name if self.role == 'staff' else self.restaurant_name

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    unit = db.Column(db.String(20), nullable=False)
    min_threshold = db.Column(db.Float, nullable=False, default=5.0)
    unit_cost = db.Column(db.Float, nullable=False, default=0.0) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # ---> FASE 28: DETTAGLI RICETTA AVANZATA <---
    prep_time = db.Column(db.Integer, nullable=True) # Tempo in minuti
    allergens = db.Column(db.String(200), nullable=True) # Es: Glutine, Lattosio
    instructions = db.Column(db.Text, nullable=True) # Procedimento
    image_file = db.Column(db.String(150), nullable=False, default='default.jpg') # Foto
    
    recipes = db.relationship('RecipeItem', backref='menu_item', lazy=True, cascade="all, delete-orphan")

class RecipeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity_needed = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')

class ConsumptionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity_used = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product')