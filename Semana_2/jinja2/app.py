from flask import Flask, redirect, render_template, request, url_for, flash

app = Flask(__name__)

app.secret_key = 'hash' #Em produção não (usa chave hex do import secret e adiciona no OS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'Thiago' and request.form['password'] == '123456':
            flash('Login realizado com sucesso!', '1')
            return redirect(url_for('index'))
        else:
            flash('Falha ao realizar o login!', '2')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flash('Deslogado com sucesso!', '3')
    return redirect(url_for('index'))

@app.route('/contato', methods=['GET', 'POST'])
def contato():
# Se o formulário for enviado (método POST)
    if request.method == 'POST':
        # Pega os dados dos campos do formulário
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        # Por enquanto, vamos apenas imprimir no terminal para ver se funcionou
        print(f'Nova mensagem de {nome} ({email}): {mensagem}')
        # Redireciona o usuário para uma página de sucesso
        return redirect(url_for('sucesso'))
    # Se a página for apenas carregada (método GET), mostra o formulário
    return render_template('contato.html')

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)