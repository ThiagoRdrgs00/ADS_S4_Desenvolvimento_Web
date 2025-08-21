from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField  # Importação do SelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email
from wtforms import ValidationError
from datetime import date
import os

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# --- Definição do Formulário com WTForms ---
class EventoForm(FlaskForm):
    """Define os campos e validadores para o formulário de evento."""
    nome_evento = StringField(
        'Nome do Evento',
        validators=[DataRequired(message="O nome do evento é obrigatório.")]
    )
    tipo_evento = SelectField(
        'Tipo do Evento',
        choices=[
            ('1', 'Palestra'),
            ('2', 'Workshop'),
            ('3', 'Meetup'),
            ('4', 'Outro')
        ],
        validators=[DataRequired(message="O tipo do evento é obrigatório.")]
    )
    data_evento = DateField(
        'Data do Evento',
        format='%Y-%m-%d',
        validators=[DataRequired(message="A data do evento é obrigatória.")]
    )
    organizador = StringField(
        'Organizador',
        validators=[DataRequired(message="O nome do organizador é obrigatório.")]
    )
    email = StringField(
        'E-mail',
        validators=[
            DataRequired(message="O campo e-mail é obrigatório."),
            Email(message="Por favor, insira um e-mail válido.")
        ]
    )
    mensagem = TextAreaField('Mensagem')  # Renomeado de mensagem para descricao
    enviar = SubmitField('Enviar')

    def validate_data_evento(self, field):
        if field.data and field.data < date.today():
            raise ValidationError("A data do evento não pode ser no passado.")

    def validate_mensagem(self, field):
        # Se o tipo_evento for '4' (Outro), descricao é obrigatória
        if self.tipo_evento.data == '4' and (not field.data or not field.data.strip()):
            raise ValidationError("A descrição é obrigatória quando o tipo do evento é 'Outro'.")

# --- Definição de um Objeto para Simulação ---
class Usuario:
    def __init__(self, nome, email, mensagem=""):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

# --- Rotas da Aplicação ---
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/vazio", methods=['GET', 'POST'])
def formulario_vazio():
    """Cenário 1: Formulário Vazio."""
    form = EventoForm()
    if form.validate_on_submit():
        nome_usuario = form.organizador.data
        return render_template('sucesso.html', nome_usuario=nome_usuario)
    return render_template(
        'formulario.html',
        form=form,
        title="1. Formulário Vazio"
    )

@app.route("/via-argumentos", methods=['GET', 'POST'])
def formulario_via_argumentos():
    """Cenário 2: Formulário Preenchido via Argumentos."""
    form = EventoForm()
    if form.validate_on_submit():
        nome_usuario = form.organizador.data
        return render_template('sucesso.html', nome_usuario=nome_usuario)
    elif not form.is_submitted():
        dados_iniciais = {
            'nome_evento': 'Workshop Python',
            'data_evento': '2025-08-30',
            'organizador': 'João da Silva',
            'email': 'joao.silva@email.com',
            'descricao': 'Esta é uma mensagem preenchida por argumentos.'  # Alterado para descricao
        }
        form = EventoForm(**dados_iniciais)
    return render_template(
        'formulario.html',
        form=form,
        title="2. Formulário Preenchido via Argumentos"
    )

@app.route("/via-objeto", methods=['GET', 'POST'])
def formulario_via_objeto():
    """Cenário 3: Formulário Preenchido via Objeto."""
    form = EventoForm()
    if form.validate_on_submit():
        nome_usuario = form.organizador.data
        return render_template('sucesso.html', nome_usuario=nome_usuario)
    elif not form.is_submitted():
        usuario_mock = Usuario(
            nome="Maria Oliveira",
            email="maria.o@email.net",
            mensagem="Mensagem vinda de um objeto."
        )
        dados_iniciais = {
            'nome_evento': 'Encontro de Dados',
            'data_evento': '2025-09-10',
            'organizador': usuario_mock.nome,
            'email': usuario_mock.email,
            'descricao': usuario_mock.mensagem  # Alterado para descricao
        }
        form = EventoForm(**dados_iniciais)
    return render_template(
        'formulario.html',
        form=form,
        title="3. Formulário Preenchido via Objeto"
    )

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)