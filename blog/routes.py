import os
import secrets
from PIL import Image
from flask import request, render_template, url_for, redirect, flash, abort
from blog import app, db, bcrypt, login_manager, mail
from blog.modelos import Usuario, Post
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/home")
@app.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.fecha.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", title="Blogando", posts=posts)


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Usuario.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(autor=user).order_by(
        Post.fecha.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data,
                    contenido=form.contenido.data,
                    autor=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Publicacion creada correctamente.', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title="Nueva publicacion", form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', titulo=post.titulo, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def upadate_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.contenido = form.contenido.data,
        db.session.commit()
        flash('Publicacion actualizada.', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.titulo.data = post.titulo
        form.contenido.data = post.contenido
    return render_template('create_post.html', title='Actualizar publicación', form=form, legend='Actualizar publicación')


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Publicación eliminada', 'success')
    return redirect(url_for('home'))


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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Imploración de cambio de contraseña',
                  sender='noreply@nomail.com', recipients=[user.email])
    msg.body = f'''Para cambiar tu contraseña pulsa el siguiente enlace:
        {url_for('reset_token', token=token, _external=True)}
        Si no deseas cambiar la contraseña, simplemente ignora este mensaje (no te sepa mal hacerme trabajar para nada...)
        '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Si tu correo está en nuestra base de datos, se mandará un correo con las instrucciones a seguir.', 'info')
        return redirect(url_for('home'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Usuario.verify_reset_token(token)
    if user is None:
        flash('Enlace no valido o expirado', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Contraseña actualizada, a ver si esta no se te olvida...', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Actualizar contraseña', form=form)


@app.route("/gaslands")
@app.route("/gas")
def aboutisasion():
    return "<p>About y eso</p>"
