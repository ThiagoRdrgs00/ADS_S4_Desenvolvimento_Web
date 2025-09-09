import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------------------#
db = SQLAlchemy(app)

receita_ingrediente = db.Table('receita_ingrediente',
    db.Column('id_receita', db.Integer, db.ForeignKey('receita.id'), primary_key=True),
    db.Column('id_ingrediente', db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
)

class Chef(db.Model):
    __tablename__ = 'chef'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)

    perfilChef_chef = db.relationship('PerfilChef', uselist=False, back_populates='chef_perfilChef', cascade='all, delete-orphan')

    receita_chef = db.relationship('Receita', back_populates='chef_receita', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Chef {self.nome}>'
    
class PerfilChef(db.Model):
    __tablename__ = 'perfil_chef'
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(80), unique=True, nullable=False)
    anos_experiencia = db.Column(db.Integer, nullable=False)

    id_chef = db.Column(db.Integer, db.ForeignKey('chef.id'), unique=True, nullable=False)
    chef_perfilChef = db.relationship('Chef', back_populates='perfilChef_chef')

    def __repr__(self):
        return f'<PerfilChef for {self.chef.nome}>'

class Receita(db.Model):
    __tablename__ = 'receita'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), unique=True, nullable=False)

    id_chef = db.Column(db.Integer, db.ForeignKey('chef.id'), unique=True, nullable=False)
    chef_receita = db.relationship('Chef', back_populates='receita_chef')

    receitas = db.relationship('Ingrediente', secondary=receita_ingrediente, back_populates='ingredientes', lazy='dynamic')

    def __repr__(self):
        return f'<Receita {self.titulo}>'
    
class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    
    ingredientes = db.relationship('Receita', secondary=receita_ingrediente, back_populates='receitas', lazy='dynamic')

    def __repr__(self):
        return f'<Ingrediente {self.nome}>'
#----------------------------------------------------------------------------------------#

@app.route('/')
def index():
    # Busca todos os usuários e os perfis associados (graças ao 'relationship')
    chefs = Chef.query.all()
    # Busca usuários que ainda não têm um perfil para popular o formulário de criação de perfil
    usuarios_sem_perfil = Usuario.query.filter(Usuario.perfil == None).all()
    
    # O HTML é renderizado a partir de uma string para manter tudo em um único arquivo
    return render_template('index.html', usuarios=usuarios, usuarios_sem_perfil=usuarios_sem_perfil)

if __name__ == '__main__':
    # Cria as tabelas no banco de dados, se não existirem
    with app.app_context():
        db.create_all()

    app.run(debug=True,port=5000)