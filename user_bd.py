import pyodbc


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
    print("Conexão com o banco de dados do usuário bem Sucedida")
    cursor = conexao.cursor()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados do usuario: {e}")

#funções para o banco de dados do usuario

class dados_user:
    def __init__(self, nome, sobrenome, email, senha=None):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha

    def cadastrar_usuario(self):

        comando = f"""INSERT INTO DimUser(nome_user, sobrenome_user, email_user, senha_user)
                  VALUES ('{self.nome}', '{self.sobrenome}', '{self.email}', '{self.senha}')"""
        cursor.execute(comando)
        cursor.commit()

    
    
def localizar_usuario(email):
    comando = f"""SELECT * FROM DimUser WHERE email_user = '{email}'"""
    cursor.execute(comando)
    return cursor.fetchall()
    
def deletar_usuario(email):
    comando = f"""DELETE FROM DimUser WHERE email_user = '{email}'"""
    cursor.execute(comando)
    cursor.commit()

def identificar_usuario(email):
    comando = f"""SELECT id_user FROM DimUser WHERE email_user = '{email}'"""
    cursor.execute(comando)
    return cursor.fetchall()

def identificar_agente(nome):
    comando = f"""SELECT key_agent FROM DimAgent WHERE nome_agente = '{nome}'"""
    cursor.execute(comando)
    return cursor.fetchall()