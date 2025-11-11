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

# methods=[GET] significa che questa funzione risponde solo quando un utente visita (GET) la pagina. Stiamo così dicendo:
# "Quando qualcuno visita/add, mostragli add_product.html"