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
    app = Flask(__name__)

    # Configurazione di base presa dal file .env
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Colleghiamo il database all'app
    db.init_app(app)

    # Configurazione Login (per l'area riservata del ristoratore)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Nome della futura rotta di login
    login_manager.init_app(app)

    # Rotta di prova per vedere se tutto funziona
    @app.route('/')
    def index():
        return "<h1>S.I.M. - Benvenuto nell'Inventory Management!</h1><p>Il motore Flask è acceso.</p>"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)