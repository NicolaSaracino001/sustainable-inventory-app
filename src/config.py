import os

# Troviamo il percorso base della nostra cartella 'src'
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Set Flask configuration variables."""

    # Impostazione chiave per SQLAlchemy: dove salvare il database
    # Creerà un file 'database.db' all'interno della cartella 'src'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

    # Disattiviamo una funzione di SQLAlchemy che non ci serve 
    # e che consuma risorse
    SQLALCHEMY_TRACK_MODIFICATIONS = False