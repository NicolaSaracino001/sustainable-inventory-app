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
    # Per ora, mandiamo un semplice messaggio
    # In futuro, qui caricheremo il file dashboard.html
    return "<h1>Dashboard (in costruzione!)</h1>"

# (Nota: importiamo render_template anche se non lo usiamo ancora,
# ci servirà tra poco)