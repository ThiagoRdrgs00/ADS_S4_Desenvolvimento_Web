from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

lista_tarefas = []

@app.route('/')
def index():
    return render_template('index.html', tarefas=lista_tarefas)

@app.route('/sucesso', methods=['POST'])
def sucesso():
    global lista_tarefas
    tarefa = request.form['tarefa']
    data = request.form['data']

    if tarefa:
        texto_tarefa = f"{tarefa} - {data}"
        lista_tarefas.append(texto_tarefa)
        return render_template('sucesso.html', tarefa=tarefa)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)