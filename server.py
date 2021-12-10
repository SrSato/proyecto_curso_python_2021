from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '3er5tte4b55q23c2y4afvfw41wrnp2zr84yys9ca92wam20js6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

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
    }
]


@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html", title="Blogando", posts=posts)


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html", title="Nosotros")


@app.route("/login",  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'sera' and form.password.data == '1234':
            flash('Ale, logueado!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Algo va mal...', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    form = RegistrationForm()
    if request.method == "POST" and form.validate():
        return redirect(url_for('home'))
    return render_template('registro.html', title="Registro", form=form)


@app.route("/gaslands")
@app.route("/gas")
def aboutisasion():
    return "<p>About y eso</p>"


if __name__ == '__main__':
    app.run('127.0.0.1', 3333)
