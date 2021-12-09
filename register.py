from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators


class RegistrationForm(FlaskForm):
    username = StringField('Usuario', [validators.Length(min=4, max=25)])
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Clave', [
        validators.DataRequired(),
        validators.EqualTo(
            'confirm', message='Las contraseñas deben coincidir')
    ])
    confirm = PasswordField('Repite la clave')

    submit = SubmitField('Registro')
