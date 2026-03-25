from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from src.models.models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash("Email o password errati. Riprova.")

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        restaurant_name = request.form.get('restaurant_name')
        password = request.form.get('password')

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash("Questa email è già registrata.")
            return redirect(url_for('auth.register'))

        new_user = User(email=email, full_name=full_name, restaurant_name=restaurant_name, role='owner')
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('main.dashboard'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# ---> FASE 32: PAGINA DI CAMBIO PASSWORD OBBLIGATORIO <---
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    # Se un utente arriva qui per sbaglio ma non deve cambiare password, rimandalo alla dashboard
    if not current_user.must_change_password:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if len(new_password) < 6:
            flash("La password deve contenere almeno 6 caratteri.")
        elif new_password != confirm_password:
            flash("Le password non coincidono. Riprova.")
        else:
            # Salviamo la nuova password e togliamo il "blocco"
            current_user.set_password(new_password)
            current_user.must_change_password = False
            db.session.commit()
            
            flash("✅ Password personale impostata! Benvenuto in FoodLoop.")
            return redirect(url_for('main.dashboard'))

    return render_template('change_password.html')