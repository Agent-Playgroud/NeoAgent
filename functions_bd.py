import pyodbc
import os

#conexão com o banco de dados

try:
    dados_conexao = (
        "Driver={SQL Server};"
        "Server=MAQ-RR;"
        "Database=Agente_IA;"
    )

    conexao = pyodbc.connect(dados_conexao)
    print("Conexão Bem Sucedida")
    cursor = conexao.cursor()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")




#funções para o banco de dados do usuario

class dados_user:
    def __init__(self, nome, sobrenome, email, senha):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha

    def cadastrar_usuario(self):

        comando = f"""INSERT INTO DimUser(nome_user, sobrenome_user, email_user, senha_user)
                  VALUES ('{self.nome}', '{self.sobrenome}', '{self.email}', '{self.senha}')"""
        cursor.execute(comando)
        cursor.commit()

    
def listar_usuarios():
    comando = f"""SELECT * FROM DimUser"""
    cursor.execute(comando)
    return cursor.fetchall()
    
def localizar_usuario(email):
    comando = f"""SELECT * FROM DimUser WHERE email_user = '{email}'"""
    cursor.execute(comando)
    return cursor.fetchall()
    
def deletar_usuario(email):
    comando = f"""DELETE FROM DimUser WHERE email_user = '{email}'"""
    cursor.execute(comando)
    cursor.commit()

def atualizar_usuario(email, nome, sobrenome, senha):
    comando = f"""UPDATE DimUser SET nome_user = '{nome}', sobrenome_user = '{sobrenome}', senha_user = '{senha}' WHERE email_user = '{email}'"""
    cursor.execute(comando)
    cursor.commit()



#funções para o banco de dados do agente

class dados_agent:
    def __init__(self, nome, tema):
        self.nome = nome
        self.tema = tema

    def cadastrar_agente(self):
        comando = f"""INSERT INTO DimAgent(nome_agente, tema_agente)
                  VALUES ('{self.nome}', '{self.tema}')"""
        cursor.execute(comando)
        cursor.commit()
        caminho = os.getcwd()
        os.makedirs(f"{caminho}/agentes/{self.nome}")

        

def listar_agentes():
    comando = f"""SELECT * FROM DimAgent"""
    cursor.execute(comando)
    return cursor.fetchall()


def localizar_agente(nome):
    comando = f"""SELECT * FROM DimAgent WHERE nome_agente = '{nome}'"""
    cursor.execute(comando)
    return cursor.fetchall()

def deletar_agente(nome):
    comando = f"""DELETE FROM DimAgent WHERE nome_agente = '{nome}'"""
    cursor.execute(comando)
    cursor.commit()

def atualizar_agente(nome, tema):
    comando = f"""UPDATE DimAgent SET tema_agente = '{tema}' WHERE nome_agente = '{nome}'"""
    cursor.execute(comando)
    cursor.commit()    