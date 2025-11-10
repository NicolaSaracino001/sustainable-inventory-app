from .. import db # Importiamo l'oggetto 'db' dal file __init__.py
from datetime import datetime

class Product(db.Model):
    """
    Modello del Prodotto per il database.
    """

    # Nome della tabella nel database
    __tablename__ = 'product'

    # Definiamo le colonne
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0)
    cost_per_unit = db.Column(db.Float, nullable=True)

    # Il campo più importante per l'MVP!
    expiry_date = db.Column(db.DateTime, nullable=False)

    added_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # Questo aiuta nel debug, per vedere il nome del prodotto
        return f'<Product {self.name}>'