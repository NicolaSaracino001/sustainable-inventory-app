from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models.user import User # Per controllare se l'email esiste già

class RegistrationForm(FlaskForm):
    """Modulo di Registrazione Utente."""
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrati')

    def validate_username(self, username):
        """Controlla se l'username è già in uso."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username già in uso. Scegline un altro.')

    def validate_email(self, email):
        """Controlla se l'email è già in uso."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email già in uso. Scegline un\'altra.')


class LoginForm(FlaskForm):
    """Modulo di Login Utente."""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ricordami')
    submit = SubmitField('Login')