import pymysql

print('Conectando...')

conn = pymysql.connect(user='root', passwd='root', host='localhost', port=3306)

# Descomente se quiser desfazer o banco...
conn.cursor().execute("DROP DATABASE `gpmio`;")
conn.commit()

criar_tabelas = '''SET NAMES utf8;CREATE DATABASE `gpmio`; USE `gpmio`;CREATE TABLE `projeto` (`id` int(11) NOT NULL AUTO_INCREMENT,`nome` varchar(50) COLLATE utf8_bin NOT NULL,      `descricao` text COLLATE utf8_bin NOT NULL,      `lider` varchar(100) COLLATE utf8_bin NOT NULL,      `github` varchar(100) COLLATE utf8_bin NOT NULL,      `url` varchar(100) COLLATE utf8_bin NOT NULL,            PRIMARY KEY (`id`)    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;    CREATE TABLE `usuario` (      `id` varchar(8) COLLATE utf8_bin NOT NULL,      `nome` varchar(20) COLLATE utf8_bin NOT NULL,      `senha` varchar(8) COLLATE utf8_bin NOT NULL,      PRIMARY KEY (`id`)    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
'''

cursor = conn.cursor()
# Dividir os comandos SQL separados por ';'
comandos = criar_tabelas.split(';')

# Executar cada comando individualmente
for comando in comandos:
    if comando.strip() != '':
        cursor.execute(comando)

# Fechar o cursor e commitar as alterações
cursor.close()

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO gpmio.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('ibsem', 'Ibsem Dias', '1234'),
            ('root', 'Root', 'root')
      ])

cursor.execute('select * from gpmio.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo projetos
cursor.executemany(
      'INSERT INTO gpmio.projeto (nome, descricao, lider, github, url) VALUES (%s, %s, %s, %s, %s)',
      [
            ('EasyChurras',
             'O Elas é um aplicativo de alerta de abuso sexual com geolocalização para notificar imediatamente a polícia quando a vítima se sentir em perigo. O projeto esta sendo feito como forma de um trabalho da faculdade, mas esperamos conseguir levar a ideia adiante e ajudar diversas pessoas que possam passar por tentativas ou crimes de abuso. O objetivo do aplicativo é notificar a policia por meio de uma API. O aplicativo é destinado a todas as pessoas que sofrem, já sofreram ou tenham medo de serem vítimas de violência sexual ou doméstica.',
             'Keliven',
             'https://github.com/iKeliven/EasyChurras',
             ''),
            ('Fin4Teen', 'Desenvolver um Aplicativo Mobile Android, '
            ,'','',''),
            ('Elas ','O Elas é um aplicativo de alerta de abuso sexual c',
            '','',''),
            ('Vamos Jogar','Rede social para praticantes de esportes coletivos',
            '','',''),
            ('LinkMe', 'As soluções de hoje tentam atender as vagas e aos candidatos de diversos setores'
            ,'','',''),
            ('PODI', 'Aplicativo de gerenciamento de filas de atendimento hospitalares', '', '',''),
      ])

cursor.execute('select * from gpmio.projeto')
print(' -------------  Projetos:  -------------')
for projeto in cursor.fetchall():
    print(projeto[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()
