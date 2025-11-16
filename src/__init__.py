from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # <-- 1. NUOVO IMPORT
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager() # <-- 2. INIZIALIZZA LOGIN MANAGER

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app) # <-- 3. COLLEGA LOGIN MANAGER ALL'APP

    # Diciamo a Flask-Login qual è la pagina di login
    login_manager.login_view = 'auth_bp.login' 
    # Messaggio da mostrare se si prova ad accedere a una pagina protetta
    login_manager.login_message = 'Devi effettuare il login per vedere questa pagina.'
    login_manager.login_message_category = 'danger' # Usa la nostra classe CSS per i flash

    with app.app_context():
        # Importa i modelli
        from .models import product, log, user # <-- 4. AGGIUNGI 'user'

        db.create_all() 

        # Importa e registra le rotte
        from .routes import inventory
        app.register_blueprint(inventory.inventory_bp)

        # (Aggiungeremo le rotte di 'auth' qui tra poco)

        return app