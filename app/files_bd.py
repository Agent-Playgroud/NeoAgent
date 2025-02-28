import pyodbc

#conexão com o banco de dados

try:
    dados_conexao = (
        "Driver={SQL Server};"
        "Server=MAQ-RR;"
        "Database=Agente_IA;"
        "Trusted_Connection=yes;"
        "Timeout=600;"
    )

    conexao = pyodbc.connect(dados_conexao)
    print("Conexão com banco de dados dos arquivos bem sucedida")
    cursor = conexao.cursor()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados dos arquivos: {e}")



#funções para o banco de dados dos arquivos

def inserir_arquivo(id_agente,nome_arquivo,id_user):
    comando = f"""INSERT INTO DimAgent(key_agente,file_source, id_user)
                VALUES ('{id_agente}', '{nome_arquivo}', '{id_user}')"""
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

def listar_arquivos(id_user,id_agente):
    comando = f"""SELECT file_source FROM FactSourceAgent where id_user = '{id_user}' AND key_agent = '{id_agente}'"""
    cursor.execute(comando)
    return cursor.fetchall()



    