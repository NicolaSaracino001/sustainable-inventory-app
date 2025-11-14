from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Inizializza l'estensione del database
db = SQLAlchemy()

def create_app():
    """Costruisce il core dell'applicazione Flask."""

    app = Flask(__name__)

    # Carica la configurazione dal file config.py
    app.config.from_object(Config)

    # Inizializza il database con la nostra app
    db.init_app(app)

    # Con questo 'with' ci assicuriamo che tutto sia 
    # pronto prima di importare le rotte
    with app.app_context():
        # Importa i modelli del database 
        from .models import product, log 
        # Crea tutte le tabelle del database
        db.create_all()
        #... (codice successivo) ...

        # Crea tutte le tabelle del database (se non esistono già)
        db.create_all() 

        # Importa e registra le rotte (Blueprints)
        from .routes import inventory
        app.register_blueprint(inventory.inventory_bp)

        return app