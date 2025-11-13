# 1. IMPORTA 'flash' da Flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from .. import db 
from .. models.product import Product 

inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='../templates', 
    static_folder='../static'      
)

@inventory_bp.route('/')
def dashboard():
    products = Product.query.order_by(Product.expiry_date.asc()).all()
    return render_template("dashboard.html", products=products, today=date.today())


@inventory_bp.route('/add', methods=['GET', 'POST'])
def add_product_page():

    if request.method == 'POST':
        name = request.form.get('product_name')
        quantity = request.form.get('product_quantity')
        cost = request.form.get('product_cost')
        expiry_date_str = request.form.get('product_expiry')

        quantity_float = float(quantity) if quantity else 0
        cost_float = float(cost) if cost else None
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()

        new_product = Product(
            name=name,
            quantity=quantity_float,
            cost_per_unit=cost_float,
            expiry_date=expiry_date
        )

        db.session.add(new_product)
        db.session.commit()

        # 2. MESSAGGIO FLASH DI SUCCESSO
        flash('Prodotto aggiunto con successo!', 'success')

        return redirect(url_for('inventory_bp.dashboard'))

    return render_template("add_product.html")


@inventory_bp.route('/delete/<int:product_id>')
def delete_product(product_id):
    product_to_delete = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()

        # 3. MESSAGGIO FLASH DI PERICOLO/ELIMINAZIONE
        flash('Prodotto eliminato.', 'danger')

        return redirect(url_for('inventory_bp.dashboard'))
    except:
        return "Errore durante l'eliminazione del prodotto."


@inventory_bp.route('/update_stock/<int:product_id>', methods=['POST'])
def update_stock(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        quantity_to_remove = float(request.form.get('quantity_to_update'))
        action = request.form.get('action') 

        if quantity_to_remove > 0:
            if action == 'use' or action == 'waste':
                if product.quantity >= quantity_to_remove:
                    product.quantity -= quantity_to_remove
                else:
                    product.quantity = 0

                db.session.commit()

                # 4. MESSAGGIO FLASH INFORMATIVO
                flash('Quantità aggiornata!', 'info')

    except ValueError:
        flash('Quantità non valida.', 'danger') 

    return redirect(url_for('inventory_bp.dashboard'))