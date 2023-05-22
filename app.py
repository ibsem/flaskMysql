#coding: utf-8
from flask import Flask, render_template, request, redirect, session, flash, url_for
import pymysql
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'cesusc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/gpmio'
db = SQLAlchemy(app)


class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    lider = db.Column(db.String(100), nullable=False)
    github = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
    projetos = Projeto.query.all()
    return render_template('lista.html', titulo='Projetos', projetos=projetos)


@app.route('/bot')
def bot():
    return render_template('bot.html', titulo='Respostas BOT')


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Projeto')


@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    descricao = request.form['descricao']
    lider = request.form['lider']
    github = request.form['github']
    url = request.form['url']
    projeto = Projeto(nome=nome, descricao=descricao, lider=lider, github=github, url=url)
    db.session.add(projeto)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('index')))
    projeto = Projeto.query.get(id)
    return render_template('editar.html', titulo='Editando Projeto', projeto=projeto)




@app.route('/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    projeto = Projeto.query.get(id)
    projeto.nome = request.form['nome']
    projeto.descricao = request.form['descricao']
    projeto.lider = request.form['lider']
    projeto.github = request.form['github']
    projeto.url = request.form['url']
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('index')))
    projeto = Projeto.query.get(id)
    db.session.delete(projeto)
    db.session.commit()
    flash('Projeto deletado com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuario.query.get(request.form['usuario'])
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
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
