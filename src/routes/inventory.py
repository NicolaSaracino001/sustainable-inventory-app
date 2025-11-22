from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime, date
# 1. IMPORTIAMO 'func' DIRETTAMENTE DA QUI
from sqlalchemy import or_, func
# 2. Da qui importiamo SOLO 'db'
from .. import db 
from ..models.product import Product 
from ..models.log import Log

from ..models.log import Log

# DIZIONARIO DEI CONSIGLI !!
CATEGORY_TIPS = {
    'meat': "⚠️ Rischio alto! Cucina subito (es. Ragù, Polpette, Brodo) o congela immediatamente se non è già stato scongelato.",
    'dairy': "🥛 Ottimo per dolci da forno, besciamella, quiche salate o per mantecare la pasta.",
    'fruit_veg': "🥗 Non buttare! Fai minestroni, vellutate, frullati, marmellate o salse.",
    'bakery': "🍞 Se è secco: fanne Pangrattato, Crostini, Bruschette o la classica Torta di pane.",
    'dry': "📦 Verifica solo che la confezione sia integra e non ci siano farfalline. Spesso commestibile anche dopo la data.",
    'general': "🔎 Controlla attentamente odore, colore e consistenza prima dell'uso."
}


inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='../templates', 
    static_folder='../static'      
)

@inventory_bp.route('/')
@login_required
def dashboard():
    search_query = request.args.get('search')
    query = Product.query
    
    if search_query:
        query = query.filter(
            or_(
                Product.barcode == search_query,
                Product.name.contains(search_query)
            )
        )
    
    products = query.order_by(Product.expiry_date.asc()).all()
    return render_template("dashboard.html", products=products, today=date.today(), tips=CATEGORY_TIPS)


@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product_page():
    
    if request.method == 'POST':
        barcode = request.form.get('product_barcode')
        name = request.form.get('product_name')
        category = request.form.get('product_category')
        quantity = request.form.get('product_quantity')
        cost = request.form.get('product_cost')
        expiry_date_str = request.form.get('product_expiry')
        
        quantity_float = float(quantity) if quantity else 0
        cost_float = float(cost) if cost else None
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
        
        new_product = Product(
            barcode=barcode,
            name=name,
            category=category,
            quantity=quantity_float,
            cost_per_unit=cost_float,
            expiry_date=expiry_date
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        flash('Prodotto aggiunto con successo!', 'success')
        return redirect(url_for('inventory_bp.dashboard'))
    
    return render_template("add_product.html")


@inventory_bp.route('/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product_to_delete = Product.query.get_or_404(product_id)
    
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash('Prodotto eliminato.', 'danger')
        return redirect(url_for('inventory_bp.dashboard'))
    except:
        return "Errore durante l'eliminazione del prodotto."

        
@inventory_bp.route('/update_stock/<int:product_id>', methods=['POST'])
@login_required
def update_stock(product_id):
    product = Product.query.get_or_404(product_id)
    
    try:
        quantity_to_remove = float(request.form.get('quantity_to_update'))
        action = request.form.get('action') 
        
        if quantity_to_remove > 0 and (action == 'use' or action == 'waste'):
            
            if product.quantity >= quantity_to_remove:
                product.quantity -= quantity_to_remove
            else:
                quantity_to_remove = product.quantity
                product.quantity = 0
            
            new_log_entry = Log(
                action_type=action,
                product_name=product.name,
                quantity=quantity_to_remove,
                product_id=product.id,
                cost_per_unit=product.cost_per_unit 
            )
            
            db.session.add(new_log_entry)
            db.session.commit()
            
            action_in_italiano = "Usato" if action == 'use' else "Sprecato"
            flash(f'{quantity_to_remove} unità di {product.name} registrate come "{action_in_italiano}"!', 'info')
                
    except ValueError:
        flash('Quantità non valida.', 'danger') 
        
    return redirect(url_for('inventory_bp.dashboard'))


@inventory_bp.route('/report')
@login_required
def report_page():
    # 1. Recupera tutti i record
    log_entries = Log.query.order_by(Log.timestamp.desc()).all()
    
    # 2. CALCOLA I TOTALI QUANTITÀ
    total_used_quantity = db.session.query(func.sum(Log.quantity)).filter(Log.action_type == 'use').scalar() or 0
    total_wasted_quantity = db.session.query(func.sum(Log.quantity)).filter(Log.action_type == 'waste').scalar() or 0
    
    # 3. CALCOLA I TOTALI COSTI
    total_used_cost = db.session.query(func.sum(Log.quantity * Log.cost_per_unit)).filter(Log.action_type == 'use').scalar() or 0
    total_wasted_cost = db.session.query(func.sum(Log.quantity * Log.cost_per_unit)).filter(Log.action_type == 'waste').scalar() or 0
    
    # 4. CLASSIFICHE (Top 5)
    top_used_products = db.session.query(
        Log.product_name, 
        func.sum(Log.quantity).label('total_qty')
    ).filter(Log.action_type == 'use') \
     .group_by(Log.product_name) \
     .order_by(func.sum(Log.quantity).desc()) \
     .limit(5).all()

    top_wasted_products = db.session.query(
        Log.product_name, 
        func.sum(Log.quantity).label('total_qty')
    ).filter(Log.action_type == 'waste') \
     .group_by(Log.product_name) \
     .order_by(func.sum(Log.quantity).desc()) \
     .limit(5).all()

    return render_template(
        "report.html", 
        log_entries=log_entries,
        total_used_quantity=total_used_quantity,
        total_wasted_quantity=total_wasted_quantity,
        total_used_cost=total_used_cost,
        total_wasted_cost=total_wasted_cost,
        top_used_products=top_used_products,
        top_wasted_products=top_wasted_products
    )