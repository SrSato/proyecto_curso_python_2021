from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class PostForm(FlaskForm):
    titulo = StringField(
        'Título',
        [validators.DataRequired(message="Dale un título a tu publicación.")])
    contenido = StringField(
        'Contenido',
        [validators.DataRequired(message="No dejes vacía la publicación")])
    submit = SubmitField('Publicar')
