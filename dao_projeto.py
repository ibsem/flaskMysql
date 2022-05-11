from models_projeto import Projeto, Usuario

SQL_DELETA_PROJETO = 'delete from projeto where id = %s'
SQL_PROJETO_POR_ID = 'SELECT id, nome, descricao, lider, github, url from projeto where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_PROJETO = 'UPDATE projeto SET nome=%s, descricao=%s, lider=%s, github=%s, url=%s where id = %s'
SQL_BUSCA_PROJETOS = 'SELECT id, nome, descricao, lider, github, url from projeto'
SQL_CRIA_PROJETO = 'INSERT into projeto (nome, descricao, lider, github, url) values (%s, %s, %s,%s,%s)'


class ProjetoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, projeto):
        cursor = self.__db.connection.cursor()

        if (projeto.id):
            cursor.execute(SQL_ATUALIZA_PROJETO, (projeto.nome, projeto.descricao, projeto.lider, projeto.github, projeto.url, projeto.id))
        else:
            cursor.execute(SQL_CRIA_PROJETO, (projeto.nome, projeto.descricao, projeto.lider, projeto.github, projeto.url))
            projeto.id = cursor.lastrowid
        self.__db.connection.commit()
        return projeto

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_PROJETOS)
        projetos = traduz_projetos(cursor.fetchall())
        return projetos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_PROJETO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Projeto(tupla[1], tupla[2], tupla[3],tupla[4], tupla[5], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_PROJETO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_projetos(projetos):
    def cria_projeto_com_tupla(tupla):
        return Projeto(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])
    return list(map(cria_projeto_com_tupla, projetos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
