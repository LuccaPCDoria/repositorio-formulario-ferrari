from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "chave_secreta_ferrari"

# Configuração do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",  # seu usuário MySQL
    password="mamapapa2901",  # sua senha MySQL
    database="ferrari_db"
)

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

    cursor = db.cursor()
    cursor.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        flash("Email já cadastrado!", "error")
        return redirect(url_for('cadastro'))

    senha_hash = generate_password_hash(senha)
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha_hash))
    db.commit()
    flash("Usuário cadastrado com sucesso!", "success")
    return redirect(url_for('index'))

# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user['senha'], senha):
        flash(f"Bem-vindo, {user['nome']}!", "success")
        return "Login bem-sucedido!"  # depois você pode redirecionar para uma página principal
    else:
        flash("Email ou senha incorretos!", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
