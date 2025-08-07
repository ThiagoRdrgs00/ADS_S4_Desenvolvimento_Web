from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def abrirPagina():
    usuario = "Thiago"
    return render_template('index.html', usuario = usuario)

@app.route('/perfil')
@app.route('/perfil/<nome>')
def abrirPaginaPerfil(nome=None):
    usuario = nome
    if usuario == None:
        logado = False
        usuario = ""
    else:
        logado = True

    return render_template('perfil.html', usuario = usuario, logado = logado)

@app.route('/lista_produtos')
def lista_produtos():
    produtos = ['cama', 'coberta', 'travesseiro']
    return render_template('produtos.html', lista = produtos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)