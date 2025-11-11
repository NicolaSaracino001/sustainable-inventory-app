from flask import Blueprint, render_template

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
    # Questo dice a Flask: "Trova e restituisci il file 'dashboard.html'"
    return render_template("dashboard.html")


# NUOVA ROTTA per la pagina "Aggiungi Prodotto"
@inventory_bp.route('/add', methods=['GET'])
def add_product_page():
    # Questa rotta, per ora, mostra solo la pagina HTML
    return render_template("add_product.html")

# methods=[GET] significa che questa funzione risponde solo quando un utente visita (GET) la pagina. Stiamo così dicendo:
# "Quando qualcuno visita/add, mostragli add_product.html"