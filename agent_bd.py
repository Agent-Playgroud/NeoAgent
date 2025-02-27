import pyodbc
import os

#conexão com o banco de dados

try:
    dados_conexao = (
        "Driver={SQL Server};"
        "Server=MAQ-RR;"
        "Database=Agente_IA;"
        "Trusted_Connection=yes;"
        "Timeout=480;"
    )

    conexao = pyodbc.connect(dados_conexao)
    print("Conexão com o banco de dados do agente bem sucedida")
    cursor = conexao.cursor()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados dos agentes: {e}")

#funções para o banco de dados do agente

class dados_agent:
    def __init__(self, nome, tema):
        self.nome = nome
        self.tema = tema

    def cadastrar_agente(self):
        comando = f"""INSERT INTO DimAgent(key_agent,nome_agente, tema_agente)
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