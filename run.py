from src import create_app

# Creiamo l'istanza dell'applicazione
# chiamando la funzione 'create_app' che abbiamo
# scritto in src/__init__.py
app = create_app()

if __name__ == '__main__':
    # Avviamo il server
    # debug=True fa sì che il server si riavvii da solo
    # ogni volta che salviamo una modifica al codice.
    app.run(debug=True)