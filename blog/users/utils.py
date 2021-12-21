import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    print(picture_fn)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Imploración de cambio de contraseña',
                  sender='noreply@nomail.com', recipients=[user.email])
    msg.body = f'''Para cambiar tu contraseña pulsa el siguiente enlace:
        {url_for('reset_token', token=token, _external=True)}
        Si no deseas cambiar la contraseña, simplemente ignora este mensaje (no te sepa mal hacerme trabajar para nada...)
        '''
    mail.send(msg)
