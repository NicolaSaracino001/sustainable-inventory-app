from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# UserMixin è una classe speciale di Flask-Login
# che ci dà funzioni standard (es. is_authenticated)
class User(UserMixin, db.Model):
    """
    Modello dell'Utente per il database.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Non salviamo la password, ma un "hash"
    waste_budget = db.Column(db.Float, default=50.0)

    def set_password(self, password):
        """Crea un hash sicuro per la password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Controlla se la password fornita corrisponde all'hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'