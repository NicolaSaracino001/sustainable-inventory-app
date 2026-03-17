from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models.models import MenuItem, RecipeItem, Product
from src.app import db

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.restaurant_name)

@main.route('/inventory')
@login_required
def inventory():
    # In futuro qui passeremo i prodotti
    return render_template('inventory.html')

@main.route('/menu')
@login_required
def menu():
    # Recuperiamo tutti i piatti creati da questo specifico utente
    menu_items = MenuItem.query.filter_by(user_id=current_user.id).all()
    return render_template('menu.html', menu_items=menu_items)

@main.route('/add_menu_item', methods=['POST'])
@login_required
def add_menu_item():
    name = request.form.get('name')
    price = request.form.get('price')
    
    new_item = MenuItem(name=name, price=float(price), user_id=current_user.id)
    db.session.add(new_item)
    db.session.commit()
    
    flash('Piatto aggiunto al menù!')
    return redirect(url_for('main.menu'))