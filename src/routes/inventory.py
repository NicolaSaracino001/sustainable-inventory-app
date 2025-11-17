# 1a. IMPORTA 'flash' da Flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required 
from datetime import datetime, date
from .. import db 
# 1b. IMPORTA ANCHE IL NUOVO MODELLO 'Log'
from ..models.product import Product 
from ..models.log import Log
#1c. AGGIUNTA 'func' ALL'IMPORT DI 'db'
from .. import db
from sqlalchemy.sql import func

inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='../templates', 
    static_folder='../static'      
)

@inventory_bp.route('/')
@login_required 
def dashboard():
    products = Product.query.order_by(Product.expiry_date.asc()).all()
    return render_template("dashboard.html", products=products, today=date.today())


@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required 
def add_product_page():

    if request.method == 'POST':
        # ... (Nessuna modifica in questa funzione) ...
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

        flash('Prodotto aggiunto con successo!', 'success')
        return redirect(url_for('inventory_bp.dashboard'))

    return render_template("add_product.html")


@inventory_bp.route('/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    # ... (Nessuna modifica in questa funzione) ...
    product_to_delete = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash('Prodotto eliminato.', 'danger')
        return redirect(url_for('inventory_bp.dashboard'))
    except:
        return "Errore durante l'eliminazione del prodotto."


# 2. MODIFICHIAMO QUESTA FUNZIONE
@inventory_bp.route('/update_stock/<int:product_id>', methods=['POST'])
@login_required
def update_stock(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        quantity_to_remove = float(request.form.get('quantity_to_update'))
        action = request.form.get('action') # 'use' o 'waste'

        if quantity_to_remove > 0 and (action == 'use' or action == 'waste'):

            if product.quantity >= quantity_to_remove:
                product.quantity -= quantity_to_remove
            else:
                quantity_to_remove = product.quantity # Rimuovi solo quello che c'è
                product.quantity = 0

            # 3. CREIAMO IL NUOVO RECORD DI LOG
            new_log_entry = Log(
                action_type=action,
                product_name=product.name,
                quantity=quantity_to_remove,
                product_id=product.id,
                cost_per_unit=product.cost_per_unit
            )

            # 4. AGGIUNGIAMO IL LOG ALLA SESSIONE
            db.session.add(new_log_entry)

            # 5. COMMIT SALVA ENTRAMBE LE MODIFICHE
            # (sia l'aggiornamento di 'product' che il nuovo 'log_entry')
            db.session.commit()

            # Traduciamo il termine "action" prima di mostrarlo
            action_in_italiano = "Usato" if action == 'use' else "Sprecato"

            flash(f'{quantity_to_remove} unità di {product.name} registrate come "{action_in_italiano}"!', 'info')

    except ValueError:
        flash('Quantità non valida.', 'danger') 

    return redirect(url_for('inventory_bp.dashboard'))


# 3. NUOVA ROTTA PER LA PAGINA REPORT
@inventory_bp.route('/report')
@login_required 
def report_page():
    # 1. Recupera tutti i record
    log_entries = Log.query.order_by(Log.timestamp.desc()).all()

    # 2. CALCOLA I TOTALI (vecchio metodo, solo quantità)
    total_used_q = db.session.query(func.sum(Log.quantity)).filter(Log.action_type == 'use').scalar() or 0
    total_wasted_q = db.session.query(func.sum(Log.quantity)).filter(Log.action_type == 'waste').scalar() or 0

    # 3. CALCOLA I COSTI TOTALI (nuovo metodo)
    #    Questo somma (quantità * costo) per ogni riga
    total_used_cost_q = db.session.query(func.sum(Log.quantity * Log.cost_per_unit)).filter(Log.action_type == 'use').scalar() or 0
    total_wasted_cost_q = db.session.query(func.sum(Log.quantity * Log.cost_per_unit)).filter(Log.action_type == 'waste').scalar() or 0

    # 4. Passa tutti i dati al template
    return render_template(
        "report.html", 
        log_entries=log_entries,
        total_used_quantity=total_used_q,
        total_wasted_quantity=total_wasted_q,
        total_used_cost=total_used_cost_q,
        total_wasted_cost=total_wasted_cost_q
    )