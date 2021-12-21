from flask import request, render_template, Blueprint
from blog import app
from blog.modelos import Post

main = Blueprint("main", __name__)


@main.route("/home")
@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.fecha.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", title="Blogando", posts=posts)


@main.route("/nosotros")
def nosotros():
    return render_template("nosotros.html", title="Nosotros")


@main.route("/gaslands")
@main.route("/gas")
def aboutisasion():
    return "<p>About y eso</p>"
