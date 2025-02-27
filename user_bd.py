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
    print(f"Erro ao conectar ao banco de dados do usuário: {e}")

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