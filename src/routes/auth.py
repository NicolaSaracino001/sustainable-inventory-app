from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
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
            # Reindirizza sempre alla dashboard dopo il login
            return redirect(url_for('main.dashboard'))
        else:
            flash("Credenziali non valide. Riprova.")
            
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name') # Nuovo campo Nome!
        restaurant_name = request.form.get('restaurant_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash("Questa email è già registrata.")
            return redirect(url_for('auth.register'))
            
        # Creiamo il Proprietario Principale
        new_user = User(
            email=email, 
            restaurant_name=restaurant_name, 
            full_name=full_name, 
            role='owner'
        )
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