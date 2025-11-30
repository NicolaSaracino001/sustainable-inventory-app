from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
# 1. IMPORTIAMO 'func' DIRETTAMENTE DA QUI
from sqlalchemy import or_, func
# 2. Da qui importiamo SOLO 'db'
from .. import db 
from ..models.product import Product 
from ..models.log import Log

from ..models.log import Log

# Import che servono per Excel e per gestire i file in memoria
import pandas as pd # Per gestire i dati
from io import BytesIO # Per creare file in memoria
from flask import send_file # Per inviare il file all'utente


# DIZIONARIO DEI CONSIGLI !!
CATEGORY_TIPS = {
    'meat': "⚠️ Rischio alto! Cucina subito (es. Ragù, Polpette, Brodo) o congela immediatamente se non è già stato scongelato.",
    'dairy': "🥛 Ottimo per dolci da forno, besciamella, quiche salate o per mantecare la pasta.",
    'fruit_veg': "🥗 Non buttare! Fai minestroni, vellutate, frullati, marmellate o salse.",
    'bakery': "🍞 Se è secco: fanne Pangrattato, Crostini, Bruschette o la classica Torta di pane.",
    'dry': "📦 Verifica solo che la confezione sia integra e non ci siano farfalline. Spesso commestibile anche dopo la data.",
    'general': "🔎 Controlla attentamente odore, colore e consistenza prima dell'uso."
}


inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='../templates', 
    static_folder='../static'      
)

@inventory_bp.route('/')
@login_required
def dashboard():
    # --- 1. LOGICA DI RICERCA (Esistente) ---
    search_query = request.args.get('search')
    query = Product.query

    if search_query:
        query = query.filter(
            or_(
                Product.barcode == search_query,
                Product.name.contains(search_query)
            )
        )

    products = query.order_by(Product.expiry_date.asc()).all()

    # --- 2. CALCOLO DATI PER LE CARDS ---

    # Card 1: Totale Prodotti (Conta le righe)
    total_products = Product.query.count()

    # Card 2: Valore Totale Inventario (Somma Quantità * Costo)
    total_value = db.session.query(func.sum(Product.quantity * Product.cost_per_unit)).scalar() or 0

    # Card 3: Prodotti in Scadenza (nei prossimi 7 giorni)
    seven_days_from_now = date.today() + timedelta(days=7)
    expiring_soon = Product.query.filter(Product.expiry_date <= seven_days_from_now).count()

    # --- 3. GAMIFICATION: Spreco settimanale ---
    today = date.today()

    # Troviamo l'inizio della settimana corrente (Lunedì)
    start_of_week = today - timedelta(days=today.weekday())

    # Calcoliamo lo spreco totale ($) da lunedì a oggi
    weekly_waste_cost = db.session.query(func.sum(Log.quantity * Log.cost_per_unit))\
        .filter(Log.action_type == 'waste')\
        .filter(Log.timestamp >= start_of_week).scalar() or 0
    
    # Impostiamo un obiettivo (Budget di spreco massimo)
    weekly_budget = current_user.waste_budget if current_user.waste_budget else 50.0

    # Calcoliamo la percentuale per la barra di progresso (max 100%)
    waste_percentage = (weekly_waste_cost / weekly_budget) * 100
    if waste_percentage > 100: waste_percentage = 100

    return render_template(
        "dashboard.html", 
        products=products, 
        today=date.today(), 
        tips=CATEGORY_TIPS,
        # Passiamo i nuovi dati al template HTML
        total_products=total_products,
        total_value=total_value,
        expiring_soon=expiring_soon,
        weekly_waste_cost=weekly_waste_cost,
        weekly_budget=weekly_budget,
        waste_percentage=waste_percentage
    )

@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product_page():
    
    if request.method == 'POST':
        barcode = request.form.get('product_barcode')
        name = request.form.get('product_name')
        category = request.form.get('product_category')
        
        # Gestione sicura dei numeri (se vuoti mette 0)
        quantity_str = request.form.get('product_quantity')
        quantity = float(quantity_str) if quantity_str else 0.0
        
        cost_str = request.form.get('product_cost')
        cost = float(cost_str) if cost_str else None
        
        expiry_str = request.form.get('product_expiry')
        expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d').date()
        
        # 1. CERCHIAMO SE ESISTE GIÀ IL PRODOTTO (per Barcode)
        existing_product = None
        if barcode:
            existing_product = Product.query.filter_by(barcode=barcode).first()
            
        if existing_product:
            # 2. CASO A: ESISTE -> AGGIORNIAMO
            # Sommiamo la nuova quantità a quella vecchia
            existing_product.quantity += quantity
            
            # Aggiorniamo anche gli altri dati (magari il prezzo è cambiato o la scadenza è più breve)
            existing_product.name = name
            existing_product.category = category
            existing_product.cost_per_unit = cost
            # Nota: Sulla scadenza è una scelta. Di solito si tiene la più vicina o si aggiorna all'ultima.
            # Qui aggiorniamo all'ultima inserita (l'utente decide).
            existing_product.expiry_date = expiry_date
            
            flash(f'Prodotto esistente aggiornato! Nuova quantità totale: {existing_product.quantity}', 'info')
            
        else:
            # 3. CASO B: NON ESISTE -> CREIAMO NUOVO
            new_product = Product(
                barcode=barcode,
                name=name,
                category=category,
                quantity=quantity,
                cost_per_unit=cost,
                expiry_date=expiry_date
            )
            db.session.add(new_product)
            flash('Nuovo prodotto aggiunto con successo!', 'success')

        # 4. SALVIAMO LE MODIFICHE
        db.session.commit()
        
        return redirect(url_for('inventory_bp.dashboard'))
    
    return render_template("add_product.html")


@inventory_bp.route('/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product_to_delete = Product.query.get_or_404(product_id)
    
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash('Prodotto eliminato.', 'danger')
        return redirect(url_for('inventory_bp.dashboard'))
    except:
        return "Errore durante l'eliminazione del prodotto."

        
@inventory_bp.route('/update_stock/<int:product_id>', methods=['POST'])
@login_required
def update_stock(product_id):
    product = Product.query.get_or_404(product_id)
    
    try:
        quantity_to_remove = float(request.form.get('quantity_to_update'))
        action = request.form.get('action') 
        
        if quantity_to_remove > 0 and (action == 'use' or action == 'waste'):
            
            if product.quantity >= quantity_to_remove:
                product.quantity -= quantity_to_remove
            else:
                quantity_to_remove = product.quantity
                product.quantity = 0
            
            new_log_entry = Log(
                action_type=action,
                product_name=product.name,
                quantity=quantity_to_remove,
                product_id=product.id,
                cost_per_unit=product.cost_per_unit 
            )
            
            db.session.add(new_log_entry)
            db.session.commit()
            
            action_in_italiano = "Usato" if action == 'use' else "Sprecato"
            flash(f'{quantity_to_remove} unità di {product.name} registrate come "{action_in_italiano}"!', 'info')
                
    except ValueError:
        flash('Quantità non valida.', 'danger') 
        
    return redirect(url_for('inventory_bp.dashboard'))


@inventory_bp.route('/report')
@login_required
def report_page():
    # --- 1. LOGICA ESISTENTE (TOTALI E CLASSIFICHE) ---
    log_entries = Log.query.order_by(Log.timestamp.desc()).all()
    
    total_used_quantity = db.session.query(func.sum(Log.quantity)).filter(Log.action_type == 'use').scalar() or 0
    total_wasted_quantity = db.session.query(func.sum(Log.quantity)).filter(Log.action_type == 'waste').scalar() or 0
    
    total_used_cost = db.session.query(func.sum(Log.quantity * Log.cost_per_unit)).filter(Log.action_type == 'use').scalar() or 0
    total_wasted_cost = db.session.query(func.sum(Log.quantity * Log.cost_per_unit)).filter(Log.action_type == 'waste').scalar() or 0
    
    top_used_products = db.session.query(
        Log.product_name, 
        func.sum(Log.quantity).label('total_qty')
    ).filter(Log.action_type == 'use').group_by(Log.product_name).order_by(func.sum(Log.quantity).desc()).limit(5).all()

    top_wasted_products = db.session.query(
        Log.product_name, 
        func.sum(Log.quantity).label('total_qty')
    ).filter(Log.action_type == 'waste').group_by(Log.product_name).order_by(func.sum(Log.quantity).desc()).limit(5).all()

    # --- 2. NUOVA LOGICA PER IL GRAFICO A BARRE (ULTIMI 7 GIORNI) ---
    
    # Creiamo una lista degli ultimi 7 giorni (es. ['2023-10-01', '2023-10-02'...])
    dates_labels = []
    used_data_7days = []
    wasted_data_7days = []
    
    today = date.today()
    
    # Facciamo un ciclo per gli ultimi 7 giorni (da 6 giorni fa a oggi)
    for i in range(6, -1, -1):
        current_day = today - timedelta(days=i)
        dates_labels.append(current_day.strftime('%d/%m')) # Etichetta (es. 25/11)
        
        # Calcoliamo USATO per questo giorno specifico
        daily_used = db.session.query(func.sum(Log.quantity * Log.cost_per_unit))\
            .filter(Log.action_type == 'use')\
            .filter(func.date(Log.timestamp) == current_day).scalar() or 0
        used_data_7days.append(daily_used)
        
        # Calcoliamo SPRECATO per questo giorno specifico
        daily_wasted = db.session.query(func.sum(Log.quantity * Log.cost_per_unit))\
            .filter(Log.action_type == 'waste')\
            .filter(func.date(Log.timestamp) == current_day).scalar() or 0
        wasted_data_7days.append(daily_wasted)

    return render_template(
        "report.html", 
        log_entries=log_entries,
        total_used_quantity=total_used_quantity,
        total_wasted_quantity=total_wasted_quantity,
        total_used_cost=total_used_cost,
        total_wasted_cost=total_wasted_cost,
        top_used_products=top_used_products,
        top_wasted_products=top_wasted_products,
        # Passiamo i nuovi dati al template
        dates_labels=dates_labels,
        used_data_7days=used_data_7days,
        wasted_data_7days=wasted_data_7days
    )


@inventory_bp.route('/export/inventory')
@login_required
def export_inventory():
    # 1. Recupera tutti i prodotti
    products = Product.query.all()

    # 2. Crea una lista di dizionari (dati puliti)
    data = []
    for p in products:
        data.append({
            'Barcode': p.barcode,
            'Nome Prodotto': p.name,
            'Categoria': p.category,
            'Quantità': p.quantity,
            'Costo Unitario (€)': p.cost_per_unit,
            'Valore Totale (€)': (p.quantity * (p.cost_per_unit or 0)),
            'Scadenza': p.expiry_date.strftime('%Y-%m-%d')
        })

    # 3. Crea il DataFrame (la tabella Excel) con Pandas
    df = pd.DataFrame(data)

    # 4. Salva in un "buffer" di memoria (non su disco)
    output = BytesIO()
    # Usa il motore 'openpyxl' per scrivere l'Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventario Attuale')

    # Torna all'inizio del file in memoria
    output.seek(0)

    # 5. Invia il file al browser per il download
    return send_file(
        output, 
        download_name="inventario_sim.xlsx", 
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# API per l'Auto-compilazione (Memoria Prodotto)
@inventory_bp.route('/api/get_product_info/<barcode>')
@login_required
def get_product_info(barcode):
    # Cerchiamo se esiste già un prodotto con questo barcode
    # (Ne prendiamo uno qualsiasi, tanto nome e categoria sono uguali)
    product = Product.query.filter_by(barcode=barcode).first()

    if product:
        # Trovato! Restituiamo i dati
        return jsonify({
            'found': True,
            'name': product.name,
            'category': product.category,
            'cost': product.cost_per_unit
        })
    else:
        # Non trovato
        return jsonify({'found': False})
    

@inventory_bp.route('/academy')
@login_required
def academy_page():
    return render_template("academy.html")