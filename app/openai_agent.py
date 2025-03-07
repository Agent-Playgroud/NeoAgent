# -- coding: utf-8 --
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import streamlit as st
import openai  # Versão 0.28.0
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar API Key da OpenAI
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key  # Configuração para a versão 0.28.0

# Inicializar FastAPI
app = FastAPI()

# Modelo de dados para a requisição
class ChatRequest(BaseModel):
    usuario_id: str
    mensagem: str

# Função para interagir com a OpenAI
def chat_with_openai(mensagem, historico):
    """
    Função para interagir com a API da OpenAI.
    Recebe a mensagem do usuário e o histórico de conversa.
    Retorna a resposta do assistente e o histórico atualizado.
    """
    try:
        # Define o contexto do assistente (system prompt)
        system_prompt = (
            "Você é um especialista em recomendações de filmes, séries e animes. "
            "Seu objetivo é ajudar os usuários a encontrar algo interessante para assistir. "
            "Se a pergunta não for sobre esse tema, avise que só pode recomendar entretenimento "
            "e sugira que o usuário use outro chatbot."
        )
        
        # Cria a lista de mensagens para enviar à API
        mensagens = [{"role": "system", "content": system_prompt}] + historico
        mensagens.append({"role": "user", "content": mensagem})
        
        # Chama a API da OpenAI (versão 0.28.0)
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Modelo GPT-4 (ou "gpt-3.5-turbo" para versão mais rápida)
            messages=mensagens
        )
        
        # Obtém a resposta do assistente
        resposta_assistente = response['choices'][0]['message']['content']
        
        # Atualiza o histórico de conversa
        historico.append({"role": "user", "content": mensagem})
        historico.append({"role": "assistant", "content": resposta_assistente})
        
        return resposta_assistente, historico
    
    except Exception as e:
        # Em caso de erro, retorna uma mensagem de erro e o histórico atual
        return f"Erro ao chamar API: {str(e)}", historico

# Rota para recomendar filmes, séries e animes (API FastAPI)
@app.post("/recomendar")
def recomendar(chat_request: ChatRequest):
    """
    Rota FastAPI para receber uma mensagem do usuário e retornar uma recomendação.
    """
    # Inicializa o histórico de conversa (se não existir)
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Obtém a resposta do assistente
    resposta_assistente, st.session_state["messages"] = chat_with_openai(
        chat_request.mensagem, 
        st.session_state["messages"]
    )
    
    # Retorna a resposta do assistente
    return {"resposta": resposta_assistente}

# Função principal para executar o Streamlit
def main():
    """
    Função principal para a interface do Streamlit.
    """
    st.title("Agente Um - Recomendação de Filmes, Séries e Animes")
    
    # Verifica se a chave da API foi configurada
    if api_key is None:
        st.error("Erro: A chave da API da OpenAI não foi encontrada.")
        return

    # Inicializa o histórico de mensagens (se não existir)
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Exibe as mensagens anteriores
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto do usuário
    user_input = st.text_input("Digite sua pergunta ou solicitação:", key="user_input")

    # Botão para enviar a mensagem
    if st.button("Enviar"):
        if user_input:
            # Adiciona a mensagem do usuário ao histórico
            st.session_state["messages"].append({"role": "user", "content": user_input})
            
            # Chama a função para obter a resposta do assistente
            resposta_assistente, st.session_state["messages"] = chat_with_openai(
                user_input, 
                st.session_state["messages"]
            )
            
            # Adiciona a resposta do assistente ao histórico
            st.session_state["messages"].append({"role": "assistant", "content": resposta_assistente})
            
            # Atualiza a interface
            st.rerun()
        else:
            st.warning("Digite uma mensagem antes de enviar.")

    # Botão para limpar o histórico
    if st.button("Limpar Histórico"):
        st.session_state["messages"] = []
        st.rerun()

# Executa a aplicação Streamlit
if __name__ == "__main__":
    main()