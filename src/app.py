from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Carica le configurazioni dal file .env
load_dotenv()

# Inizializziamo l'oggetto Database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # CONFIGURAZIONE
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # COLLEGIAMO IL DATABASE ALL'APP
    db.init_app(app)

    # CONFIGURAZIONE LOGIN
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # QUESTA È LA PARTE MANCANTE: Il caricatore utente
    from src.models.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # REGISTRAZIONE DEI BLUEPRINTS
    from src.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Rotta di prova
    @app.route('/')
    def index():
        return "<h1>S.I.M. Acceso!</h1><a href='/login'>Vai al Login</a>"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)