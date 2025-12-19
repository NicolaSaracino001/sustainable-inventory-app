import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Set Flask configuration variables."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Torniamo alla chiave scritta in chiaro per ora
    SECRET_KEY = 'una_chiave_segreta_per_lo_sviluppo_123'