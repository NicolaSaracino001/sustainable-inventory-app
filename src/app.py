from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Carica le configurazioni dal file .env che abbiamo creato nella Fase 2
load_dotenv()

# Inizializziamo il Database (SQLAlchemy)
db = SQLAlchemy()

def create_app():
    # ... (codice esistente sopra)
    db.init_app(app)

    # Aggiungi queste righe qui sotto:
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Rotta di prova esistente
    @app.route('/')
    def index():
        return "<h1>S.I.M. Acceso!</h1><a href='/login'>Vai al Login</a>"

    return app