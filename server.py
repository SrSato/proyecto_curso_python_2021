from flask import Flask, render_template, url_for

app = Flask(__name__)

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


@app.route("/")
def home():
    return render_template("home.tem", title="blogando", posts=posts)


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html", title="nosotros")


@app.route("/gaslands")
@app.route("/gas")
def aboutisasion():
    return "<p>About y eso</p>"


app.run('127.0.0.1', 3333)
