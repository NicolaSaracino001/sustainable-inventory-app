import sys
import os

# Aggiunge la cartella corrente al percorso di ricerca di Python
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.app import create_app

app = create_app()

if __name__ == '__main__':
    # Avvia l'applicazione sulla porta 5000
    app.run(debug=True)