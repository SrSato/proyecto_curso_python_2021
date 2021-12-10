from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators


class RegistrationForm(FlaskForm):

    username = StringField(
        'Usuario', [validators.Length(min=4, max=25, message="Debe estar entre 4 y 25 caracteres")])
    email = StringField(
        'E-mail', [validators.Length(min=6, max=35, message="Debe estar entre 6 y 35 caracteres"), validators.Email(message="Escribe un mail válido.")])
    password = PasswordField('Clave', [
        validators.DataRequired(message="Campo obligatorio"),
        validators.EqualTo(
            'confirm', message='Las contraseñas deben coincidir')
    ])
    confirm = PasswordField('Repite la clave')
    submit = SubmitField('Registro')


class LoginForm(FlaskForm):
    username = StringField(
        'Usuario', [validators.Length(min=4, max=25, message="Debe estar entre 4 y 25 caracteres")])
    password = PasswordField('Clave', [
        validators.DataRequired(message="Campo obligatorio")])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Entrar')
