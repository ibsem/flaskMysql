from flask import Flask, render_template, request, redirect, session, flash, url_for
import os
import sys
cwd=os.getcwd()
sys.path.append(cwd+"/flaskMysql/")
from models_projeto import Projeto, Usuario
from dao_projeto import ProjetoDao, UsuarioDao
from flask_mysqldb import MySQL
 
app = Flask(__name__)
app.secret_key = 'cesusc'

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Mimama12."
app.config['MYSQL_DB'] = "gpmio"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)
projeto_dao = ProjetoDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista = projeto_dao.listar()
    return render_template('lista.html', titulo='Projetos', projetos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Projeto')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    descricao = request. form['descricao']
    lider = request. form['lider']
    github = request. form['github']
    url = request. form['url']
    projeto = Projeto(nome, descricao, lider, github, url)
    projeto_dao.salvar(projeto)
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    projeto = projeto_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editando Projeto', projeto=projeto)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request. form['nome']
    descricao = request. form['descricao']
    lider = request. form['lider']
    github = request. form['github']
    url = request. form['url']
    projeto = Projeto(nome, descricao, lider, github, url, request.form['id'])
    projeto_dao.salvar(projeto)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    projeto_dao.deletar(id)
    flash('Projeto deletado com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha não confere')
            return redirect(url_for('login'))
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


app.run(debug=True)
