from src import create_app

# Creiamo l'istanza dell'applicazione
# chiamando la funzione 'create_app' che abbiamo
# scritto in src/__init__.py
app = create_app()

if __name__ == '__main__':
    # Avviamo il server
    # debug=True fa sì che il server si riavvii da solo alle modifiche.
    # port=5001 serve per evitare conflitti con la porta standard del Mac (AirPlay).
    app.run(debug=True, port=5001)