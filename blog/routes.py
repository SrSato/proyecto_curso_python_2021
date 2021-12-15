import os
import secrets
from PIL import Image
from flask import request, render_template, url_for, redirect, flash
from blog import app, db, bcrypt, login_manager
from blog.modelos import Usuario, Post
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'autor': 'Pepe Gotera',
        'titulo': 'Reforma Molona',
        'fecha': '12-12-2012',
        'contenido': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Porro aut architecto iste nulla voluptatibus recusandae, eligendi laborum consequuntur quis temporibus fuga delectus nisi error id necessitatibus maiores. Fugit, nostrum corporis.',
        'color': 'fluorgreen',
        'foto': 'https://www.reformasparaviviendas.com/wp-content/uploads/2020/04/Empresa-de-reformas-integrales-en-Valencia.jpg'
    },
    {
        'autor': 'Rodolfo Langostino',
        'titulo': 'Menu Nochebuena',
        'fecha': '13-11-2011',
        'contenido': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laudantium illum officia iste, placeat ut, vitae maiores adipisci sapiente ex nisi nam delectus totam. Ducimus blanditiis impedit, maiores inventore magnam unde.',
        'color': 'fluorpink',
        'foto': "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fokdiario.com%2Fimg%2F2018%2F12%2F17%2Fmenu-recetas-de-navidad.jpg&f=1&nofb=1"
    },
    {
        'autor': 'Pepe Gotera',
        'titulo': 'Reforma Molona',
        'fecha': '12-12-2012',
        'contenido': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Porro aut architecto iste nulla voluptatibus recusandae, eligendi laborum consequuntur quis temporibus fuga delectus nisi error id necessitatibus maiores. Fugit, nostrum corporis.',
        'color': 'fluorgreen',
        'foto': 'https://www.reformasparaviviendas.com/wp-content/uploads/2020/04/Empresa-de-reformas-integrales-en-Valencia.jpg'
    },
    {
        'autor': 'Rodolfo Langostino',
        'titulo': 'Menu Nochebuena',
        'fecha': '13-11-2011',
        'contenido': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laudantium illum officia iste, placeat ut, vitae maiores adipisci sapiente ex nisi nam delectus totam. Ducimus blanditiis impedit, maiores inventore magnam unde.',
        'color': 'fluorpink',
        'foto': "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fokdiario.com%2Fimg%2F2018%2F12%2F17%2Fmenu-recetas-de-navidad.jpg&f=1&nofb=1"
    },
    {
        'autor': 'Pepe Gotera',
        'titulo': 'Reforma Molona',
        'fecha': '12-12-2012',
        'contenido': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Porro aut architecto iste nulla voluptatibus recusandae, eligendi laborum consequuntur quis temporibus fuga delectus nisi error id necessitatibus maiores. Fugit, nostrum corporis.',
        'color': 'fluorgreen',
        'foto': 'https://www.reformasparaviviendas.com/wp-content/uploads/2020/04/Empresa-de-reformas-integrales-en-Valencia.jpg'
    },
    {
        'autor': 'Rodolfo Langostino',
        'titulo': 'Menu Nochebuena',
        'fecha': '13-11-2011',
        'contenido': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laudantium illum officia iste, placeat ut, vitae maiores adipisci sapiente ex nisi nam delectus totam. Ducimus blanditiis impedit, maiores inventore magnam unde.',
        'color': 'fluorpink',
        'foto': "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fokdiario.com%2Fimg%2F2018%2F12%2F17%2Fmenu-recetas-de-navidad.jpg&f=1&nofb=1"
    }
]


@app.route("/home")
@app.route("/")
@login_required
def home():
    return render_template("home.html", title="Blogando", posts=posts)


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html", title="Nosotros")


@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash('Ale, logueado!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Algo va mal...', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        usuario = Usuario(username=form.username.data,
                          email=form.email.data, password=hashed_pass)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Cuenta de {form.username.data} creada con exito', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html', title="Registro", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    print(picture_fn)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        print(form.username.data)
        if form.picture.data:
            if current_user.image_file and current_user.image_file != 'default.jpg':
                a_borrar = os.path.join(
                    app.root_path, 'static/profile_pics', current_user.image_file)
                try:
                    os.remove(a_borrar)
                except FileNotFoundError:
                    pass
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        print(current_user.image_file)
        current_user.username = form.username.data
        current_user.email = form.email.data
        print("Comiteando")
        db.session.commit()
        flash('Cuenta actualizada, mucho más molona así...', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Mi cuenta', image_file=image_file, form=form)


@app.route("/gaslands")
@app.route("/gas")
def aboutisasion():
    return "<p>About y eso</p>"
