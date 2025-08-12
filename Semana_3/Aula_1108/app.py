# 1. Importa a classe Flask, que é a peça central da nossa aplicação.
from flask import Flask
# 2. Cria uma instância da aplicação.
# A variável __name__ informa ao Flask onde procurar por outros arquivos do projeto.
app = Flask(__name__)
# 3. Define a "rota" principal do site usando um "decorator".
# Isso significa: "Quando alguém acessar o endereço '/', execute a função logo abaixo."
@app.route('/')
def ola_mundo():
# 4. A função retorna o conteúdo (em HTML) que será exibido no navegador.
    return '<h1>Olá, Mundo! Esta é minha primeira aplicação Flask!</h1>'
# Rota para a página "Sobre"
@app.route('/sobre')
def sobre():
    return '<h2>Esta é a página Sobre</h2><p>Aqui você pode falar um pouco sobre o projeto.</p>'
# Rota para a página "Contato"
@app.route('/contato')
def contato():
    return '<h2>Fale Conosco</h2><p>Você pode entrar em contato pelo e-mail: dev@exemplo.com</p>'