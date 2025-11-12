from flask import Blueprint, render_template, request, redirect, url_for 
from datetime import datetime, date 
from .. import db #Importiamo il nostro db 
from .. models.product import Product # Importiamo il modello Product

# 1. Creiamo il 'Blueprint' (lo schema) per questo set di rotte
# Questo è l'oggetto 'inventory_bp' che __init__.py stava cercando!
inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='../templates', # Diciamo a Flask dove sono gli HTML
    static_folder='../static'      # Diciamo a Flask dove sono i CSS
)


# 2. Creiamo la nostra prima rotta (la pagina 'Home' o 'Dashboard')
# Quando un utente visita l'URL "/"
@inventory_bp.route('/')
def dashboard():
    # 1. Recupera tutti i prodotti del database ordinandoli per data di scadenza (i più vicini prima)
    products = Product.query.order_by(Product.expiry_date.asc()).all()
    # 2. Passa la lista dei prodotti al template HTML
    return render_template("dashboard.html", products=products, today=date.today())


# NUOVA ROTTA per la pagina "Aggiungi Prodotto"
@inventory_bp.route('/add', methods=['GET', 'POST'])
def add_product_page():
    # 3. AGGIUNGI questa logica per gestire l'invio
    if request.method == 'POST':
        # L'utente ha inviato il modulo, salviamo i dati!

        # Prendiamo i dati dal modulo HTML
        name = request.form.get('product_name')
        quantity = request.form.get ('product_quantity')
        cost = request.form.get ('product_cost')
        expiry_date_str = request.form.get ('product_expiry')

        # Convertiamo i dati nei formati giusti per il DB
        quantity_float = float(quantity) if quantity else 0 
        cost_float = float(cost) if cost else None 
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()

        # Creiamo un nuovo Oggetto Prodotto
        new_product = Product (
            name=name,
            quantity=quantity_float,
            cost_per_unit=cost_float,
            expiry_date=expiry_date
        )

        # Aggiungiamo il prodotto al database
        db.session.add(new_product)
        db.session.commit()

        # Rimandiamo l'utente alla dashboard
        return redirect(url_for('inventory_bp.dashboard'))
    
    # Se non è POST, è GET, quindi mostriamo solo la pagina
    return render_template("add_product.html")

# NUOVA ROTTA per Eliminare il Prodotto
@inventory_bp.route('/delete/<int:product_id>')
def delete_product(product_id):
    # 1. Trova il prodotto nel database usando l'ID, o mostra un errore 404
    product_to_delete = Product.query.get_or_404(product_id)

    try:
        # 2. Prova a eliminare il prodotto
        db.session.delete(product_to_delete)
        db.session.commit()

        # 3. Rimanda alla dashboard
        return redirect(url_for('inventory_bp.dashboard'))
    except:
        # 4. In caso di errore
        return "Errore durante l'eliminazione del prodotto."


# NUOVA ROTTA per Aggiornare la Quantità (Usato/Sprecato)
@inventory_bp.route('/update_stock/<int:product_id>', methods=['POST'])
def update_stock(product_id):
    # 1. Trova il prodotto nel database
    product = Product.query.get_or_404(product_id)

    try:
        # 2. Prendi la quantità dal modulo
        quantity_to_remove = float(request.form.get('quantity_to_update'))

        # 3. Controlla quale bottone è stato premuto
        action = request.form.get('action') # Sarà 'use' o 'waste'

        if quantity_to_remove > 0:
            # 4. Aggiorna la quantità nel database
            # Per ora, 'Usa' e 'Spreca' fanno la stessa cosa: 
            # riducono la quantità.
            if action == 'use' or action == 'waste':
                if product.quantity >= quantity_to_remove:
                    product.quantity -= quantity_to_remove
                else:
                    # Non andare in negativo, imposta a zero
                    product.quantity = 0

                # (In futuro, potremmo salvare 'action' per i report)

            db.session.commit()

    except ValueError:
        # Gestisce l'errore se l'utente non inserisce un numero valido
        pass 

    # 5. Rimanda alla dashboard
    return redirect(url_for('inventory_bp.dashboard'))