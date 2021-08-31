import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='root', host='localhost', port=3306)

# Descomente se quiser desfazer o banco...
#conn.cursor().execute("DROP DATABASE `gpmio`;")
#conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `gpmio` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `gpmio`;
    CREATE TABLE `projeto` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `descricao` varchar(100) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO gpmio.projeto (nome, descricao) VALUES ('Mercado Escolar', 'troca e venda de materiais escolares')',
      [
            ('Jogo 2D', 'Jogo Retro'),
            ('Mercado Escolar', 'troca e venda de materiais escolares', )
            
      ])

cursor.execute('select * from jogoteca.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo projetos
cursor.executemany(
      'INSERT INTO gpmio.jo (nome, categoria) VALUES (%s, %s)',
      [
            ('God of War 4', 'Ação'),
            ('NBA 2k18', 'Esporte'),
            ('Rayman Legends', 'Indie'),
            ('Super Mario RPG', 'RPG'),
            ('Super Mario Kart', 'Corrida'),
            ('Fire Emblem Echoes', 'Estratégia'),
      ])

cursor.execute('select * from gpmio.jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()