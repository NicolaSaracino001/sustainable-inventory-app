from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .. import db, login_manager
from ..models.user import User
from ..forms import LoginForm, RegistrationForm

# Creiamo il nuovo Blueprint per l'autenticazione
auth_bp = Blueprint('auth_bp', __name__)


@login_manager.user_loader
def load_user(user_id):
    """Funzione richiesta da Flask-Login per caricare l'utente dalla sessione."""
    return User.query.get(int(user_id))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    """Gestisce la registrazione di un nuovo utente."""

    # Se l'utente è già loggato, lo rimanda alla dashboard
    if current_user.is_authenticated:
        return redirect(url_for('inventory_bp.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Il modulo è valido, creiamo l'utente
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data) # Cripta la password

        # Aggiungi e salva l'utente nel DB
        db.session.add(new_user)
        db.session.commit()

        flash('Registrazione completata! Ora puoi effettuare il login.', 'success')
        return redirect(url_for('auth_bp.login_page'))

    # Se il modulo non è valido (o è la prima visita, 'GET'), mostra la pagina
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """Gestisce il login dell'utente."""

    if current_user.is_authenticated:
        return redirect(url_for('inventory_bp.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # Cerca l'utente nel DB tramite email
        user = User.query.filter_by(email=form.email.data).first()

        # Controlla se l'utente esiste E la password è corretta
        if user and user.check_password(form.password.data):
            # Utente valido, lo "logghiamo"
            login_user(user, remember=form.remember_me.data)
            flash('Login effettuato con successo!', 'success')

            # Rimanda alla pagina successiva (se c'era) o alla dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('inventory_bp.dashboard'))
        else:
            # Credenziali non valide
            flash('Login non riuscito. Controlla email e password.', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required # Solo un utente loggato può fare logout
def logout_page():
    """Gestisce il logout dell'utente."""
    logout_user()
    flash('Logout effettuato con successo.', 'info')
    return redirect(url_for('auth_bp.login_page'))