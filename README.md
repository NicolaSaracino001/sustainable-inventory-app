# S.I.M. - Sustainable Inventory Management 🍎🤖

S.I.M. è un'applicazione web gestionale progettata per la ristorazione. Aiuta a monitorare le scorte, gestire le ricette e ridurre gli sprechi alimentari grazie a un sistema di intelligenza predittiva.

## 🌟 Funzionalità Principali
- **Autenticazione Sicura:** Login e registrazione per ristoratori.
- **Magazzino Intelligente:** Inserimento materie prime con soglie di allarme personalizzate.
- **Gestione Menù e Ricette (BOM):** Creazione di piatti collegati alle materie prime in magazzino.
- **Scarico Automatico:** Sottrazione matematica degli ingredienti al momento della simulazione di un ordine.
- **Controllo Anti-Scorte Negative:** Blocco di sicurezza che impedisce la registrazione di ordini se le materie prime sono insufficienti.
- **Dashboard Grafica:** Visualizzazione istogramma (Chart.js) delle scorte e dei livelli critici.
- **Assistente Predittivo (API Meteo):** Consigli dinamici sugli acquisti basati sulle previsioni atmosferiche locali (OpenWeatherMap).

## 🛠️ Tecnologie Utilizzate
- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Login.
- **Database:** SQLite.
- **Frontend:** HTML5, CSS3, Jinja2, Chart.js.
- **Integrazioni:** API REST (OpenWeatherMap).

## 📝 Fasi Completate
- [x] Fase 1: Creazione cartelle e inizializzazione Git.
- [x] Fase 2: Configurazione .env e requirements.txt.
- [x] Fase 3: Creazione del cuore dell'app (src/app.py).
- [x] Fase 4: Definizione Modelli Database.
- [x] Fase 5: Installazione dipendenze e venv.
- [x] Fase 6: Rotte di Autenticazione (Logica).
- [x] Fase 7: Template HTML per Login e Registrazione.
- [x] Fase 8: Inizializzazione Database SQLite.
- [x] Bug Fix: Risolto NameError in `src/app.py` (ordine inizializzazione app).
- [x] Fase 9: Risoluzione ImportError e Setup degli Import Assoluti.
- [x] Bug Fix: Aggiunto `user_loader` per la gestione sessioni Flask-Login.
- [x] Fase 10: Creazione Dashboard operativa e Blueprint `main`.
- [x] Fase 11: Gestione Menù - Possibilità di aggiungere piatti al database.
- [x] Fase 12: Gestione Magazzino (Carico merci e gestione soglie).
- [x] Fase 13: La Ricetta Interattiva (Associazione Piatto -> Ingredienti).
- [x] Fase 14: Scarico Automatico - Logica di sottrazione automatica per ogni ordine.
- [x] Bug Fix: Risolto `RuntimeError` in `auth.py` usando `db.session.query`.
- [x] Bug Fix: Creato `run.py` per avvio professionale.
- [x] Bug Fix: Risolto `UndefinedError` aggiungendo la relazione tra `Product` e `RecipeItem`.
- [x] Fase 15: Sistema di Alert e Visualizzazione Colori.
- [x] Fase 16: Setup API Meteo.
- [x] Installazione libreria `requests` per comunicazioni web.
- [x] Aggiornamento `requirements.txt`.
- [x] Fase 17: Integrazione Grafici Consumi (Chart.js).
- [x] Fase 18: Sicurezza DB 
- [x] Fase 19: Revisione 
- 







