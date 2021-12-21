import os
from flask import (request, render_template, url_for, redirect, flash,
                   Blueprint, current_app)
from blog import db, bcrypt
from blog.modelos import Usuario, Post
from blog.users.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from blog.users.utils import save_picture, send_reset_email
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint("users", __name__)


@users.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash('Ale, logueado!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Algo va mal...', 'danger')
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/registro", methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        usuario = Usuario(username=form.username.data,
                          email=form.email.data, password=hashed_pass)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Cuenta de {form.username.data} creada con exito', 'success')
        return redirect(url_for('users.login'))
    return render_template('registro.html', title="Registro", form=form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        print(form.username.data)
        if form.picture.data:
            if current_user.image_file and current_user.image_file != 'default.jpg':
                a_borrar = os.path.join(
                    current_app.root_path, 'static/profile_pics', current_user.image_file)
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Mi cuenta', image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Si tu correo está en nuestra base de datos, se mandará un correo con las instrucciones a seguir.', 'info')
        return redirect(url_for('main.home'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Usuario.verify_reset_token(token)
    if user is None:
        flash('Enlace no valido o expirado', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Contraseña actualizada, a ver si esta no se te olvida...', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Actualizar contraseña', form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Usuario.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(autor=user).order_by(
        Post.fecha.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
