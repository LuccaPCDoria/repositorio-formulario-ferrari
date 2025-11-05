from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "chave_secreta_ferrari"

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect('ferrari.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página inicial (login)
@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Salvar novo usuário
@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        flash("Email já cadastrado!", "error")
        conn.close()
        return redirect(url_for('cadastro'))

    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
    conn.commit()
    conn.close()
    flash("Usuário cadastrado com sucesso!", "success")
    return redirect(url_for('index'))

# usaurios
@app.route('/usuarios')
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()

    html = "<h2>Usuários cadastrados</h2><ul>"
    for u in usuarios:
        html += f"<li>{u[1]} - {u[2]}</li>"  # nome e email
    html += "</ul>"
    return html

# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        flash("Login bem-sucedido!", "success")
        return "Login feito com sucesso!"
    else:
        flash("Email ou senha incorretos!", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Criar o banco automaticamente na primeira execução
    conn = sqlite3.connect('ferrari.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.close()

    app.run(debug=True)
