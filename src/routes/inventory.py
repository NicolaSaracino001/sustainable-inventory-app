# 1a. IMPORTA 'flash' da Flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
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
def dashboard():
    products = Product.query.order_by(Product.expiry_date.asc()).all()
    return render_template("dashboard.html", products=products, today=date.today())


@inventory_bp.route('/add', methods=['GET', 'POST'])
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
def report_page():

    # 1. Recupera tutti i record dalla tabella Log ordinandoli per data (i più recenti prima)
    log_entries = Log.query.order_by(Log.timestamp.desc()).all()

    # 2. Calcola i totali usando SQLAlchemy (func.sum) per sommare le quantità basandoci 
    # sul tipo di azione ('use' o 'waste')
    total_used_query = db.session.query(func.sum(Log.quantity)).filter(Log.action_type == 'use').scalar()
    total_wasted_query = db.session.query(func.sum(Log.quantity)).filter(Log.action_type == 'waste').scalar()

    # Gestiamo il caso in cui non ci siano dati (risulterebbe 'None')
    total_used = total_used_query if total_used_query is not None else 0 
    total_wasted = total_wasted_query if total_wasted_query is not None else 0

    # 3. Passa i record e i nuovi totali al template HTML
    return render_template("report.html", log_entries=log_entries, total_used=total_used, total_wasted=total_wasted)