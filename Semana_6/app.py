# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuApp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def __repr__(self):
        return f'<Usuario {self.email}>'

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), unique=True, nullable=False)
    descricao = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Postagem {self.titulo}>'

    def __repr__(self):
        return f'<Postagem {self.descricao}>'

# --- Rotas da Aplicação ---

# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    Usuarios = Usuario.query.all()
    return render_template('index.html', Usuarios=Usuarios)

@app.route('/postagem')
def postagem():
    Postagens = Postagem.query.all()
    return render_template('postagem.html', Postagens=Postagens)

@app.route('/adicionar', methods=['POST'])
def add_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')

    novo_usuario = Usuario(nome=nome, email=email)
    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/adicionar_postagem', methods=['POST'])
def add_postagem():
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')

    nova_postagem = Postagem(titulo=titulo, descricao=descricao)
    db.session.add(nova_postagem)
    db.session.commit()
    return redirect(url_for('postagem'))

# Passo 3: Criando o Banco de Dados Físico
if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()

    # Inicia o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5001, debug=True)