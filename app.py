from flask import Flask, send_from_directory, render_template
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv() 

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") 


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Parceiro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(200), nullable=True) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem_url = db.Column(db.String(200), nullable=False)
    link_post = db.Column(db.String(300), nullable=False)
    legenda = db.Column(db.String(200), nullable=True)


@app.route('/')
def index():
    
    todos_parceiros = Parceiro.query.all()
    
    parceiros_com_imagem = [p for p in todos_parceiros if p.logo]

    
    posts = Post.query.all()

    
    return render_template('index.html', 
                           lista_parceiros=parceiros_com_imagem, 
                           lista_posts=posts)




@app.route('/imagens/<path:filename>')
def serve_images(filename):
    return send_from_directory(directory='imagens', path=filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(directory='.', path='favicon.ico')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)