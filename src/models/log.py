from .. import db
from datetime import datetime

class Log(db.Model):
    """
    Modello per registrare ogni transazione (Uso o Spreco).
    """
    __tablename__ = 'log_entry'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 'use' (usato) o 'waste' (sprecato)
    action_type = db.Column(db.String(10), nullable=False) 

    # Nome del prodotto (lo copiamo per storico)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    # ID del prodotto originale, se esiste ancora
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)

    # Registriamo il costo per unità al momento della transazione
    cost_per_unit = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Log {self.action_type}: {self.quantity} of {self.product_name}>'