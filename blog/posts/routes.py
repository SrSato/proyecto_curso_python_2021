from flask import (request, render_template, url_for, redirect,
                   flash, abort, Blueprint)
from blog import db
from blog.modelos import Post
from blog.posts.forms import PostForm
from flask_login import current_user, login_required

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template('create_post.html',
                           title="Nueva publicacion",
                           form=form)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', titulo=post.titulo, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.contenido = form.contenido.data,
        db.session.commit()
        flash('Publicacion actualizada.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.titulo.data = post.titulo
        form.contenido.data = post.contenido
    return render_template('create_post.html',
                           title='Actualizar publicación',
                           form=form,
                           legend='Actualizar publicación')


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Publicación eliminada', 'success')
    return redirect(url_for('main.home'))
