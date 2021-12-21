import os


class Config:
    SECRET_KEY = '3er5tte4b55q23c2y4afvfw41wrnp2zr84yys9ca92wam20js6'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_MALIGNO')
    MAIL_PASSWORD = os.environ.get('CLAVE_MALIGNA')
