from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import (BooleanField, StringField, PasswordField,
                     SubmitField, validators, ValidationError)
from blog.modelos import Usuario


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Usuario',
        [validators.Length(min=4,
                           max=25,
                           message="Debe estar entre 4 y 25 caracteres")])

    email = StringField(
        'E-mail',
        [validators.Length(min=6,
                           max=35,
                           message="Debe estar entre 6 y 35 caracteres"),
         validators.Email(message="Escribe un mail válido.")])

    picture = FileField(
        'Cambiar imagen de perfil',
        validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Actualizar')

    def validate_usuario(self, username):
        if username.data != current_user.username:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError(
                    "El nombre de usuario ya está en uso, por favor, escoge otro")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = Usuario.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(
                    "Ya existe una cuenta de usuario asocidada a ese email.")


class RegistrationForm(FlaskForm):
    username = StringField(
        'Usuario',
        [validators.Length(min=4,
                           max=25,
                           message="Debe estar entre 4 y 25 caracteres")])

    email = StringField(
        'E-mail',
        [validators.Length(min=6,
                           max=35,
                           message="Debe estar entre 6 y 35 caracteres"),
         validators.Email(message="Escribe un mail válido.")])

    password = PasswordField(
        'Clave',
        [validators.DataRequired(message="Campo obligatorio"),
         validators.EqualTo(
            'confirm', message='Las contraseñas deben coincidir')
         ])

    confirm = PasswordField('Repite la clave')
    submit = SubmitField('Registro')

    def validate_usuario(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError(
                "El nombre de usuario ya está en uso, por favor, escoge otro")

    def validate_email(self, email):
        email = Usuario.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                "Ya existe una cuenta de usuario asocidada a ese email.")


class LoginForm(FlaskForm):
    username = StringField(
        'Usuario',
        [validators.DataRequired(message="Falta el nombre de usuario"),
         validators.Length(min=4, max=25, message="Debe estar entre 4 y 25 caracteres")])
    password = PasswordField('Clave', [
        validators.DataRequired(message="Campo obligatorio")])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Entrar')


class RequestResetForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(
    ), validators.Email(message='Escriba un correo electrónico')])
    submit = SubmitField('Actualizar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario is None:
            raise ValidationError('NEIN! NEIN! NEIN! NEIN! NEIN!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', [validators.DataRequired()])
    confirm_password = PasswordField('Confirmar password', [
                                     validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Actualizar')
