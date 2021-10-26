class Projeto:
    def __init__(self, nome, descricao, lider, github, url, id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.lider = lider
        self.github = github
        self.url = url
        return

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
        return