import streamlit as st
import os
import functions_bd

# Título da aplicação
st.title("Upload de Arquivos com Streamlit")

# Criando um espaço para upload
documento = st.file_uploader("Escolha um arquivo para fazer upload", type=["txt", "xlsx", "csv", "pdf"])

# Verificando se um arquivo foi enviado
if documento is not None:
    # Exibindo informações sobre o arquivo
    st.write("### Informações do arquivo:")
    st.write(f"**Nome:** {documento.name}")
    st.write(f"**Tipo:** {documento.type}")
    st.write(f"**Tamanho:** {documento.size} bytes")  

    subpasta = "agentes/Agente 1"   #PRECISAR DE ALTERAR PARA O NOME DO AGENTE
    # Salvando o arquivo no diretório "uploads/subpasta"
    caminho_arquivo = os.path.join(subpasta, documento.name)
    with open(caminho_arquivo, "wb") as f:
        f.write(documento.getbuffer())

    st.success(f"Arquivo salvo com sucesso em: {caminho_arquivo}")

    functions_bd.inserir_arquivo(1,documento.name,1)  #PRECISAR DE ALTERAR PARA O ID DO AGENTE E DO USER
