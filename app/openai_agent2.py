# -- coding: utf-8 -- 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar API Key
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Inicializar FastAPI
app = FastAPI()

# Modelo de dados para a requisição
class ChatRequest(BaseModel):
    usuario_id: str
    mensagem: str

# Função para interagir com a OpenAI
def chat_with_openai(mensagem, historico):
    """Função para interagir com a API da OpenAI"""
    try:
        system_prompt = (
    "Você é um assistente que adivinha a profissão do usuário. Faça perguntas relevantes "
    "para adivinhar qual é a profissão da pessoa. Use as respostas para ajustar as perguntas subsequentes."
)
        
        # Criar lista de mensagens para enviar à API
        mensagens = [{"role": "system", "content": system_prompt}] + historico
        mensagens.append({"role": "user", "content": mensagem})
        
        # Chamar API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=mensagens
        )
        
        # Atualizar histórico com a resposta do assistente
        historico.append({"role": "user", "content": mensagem})
        historico.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        return response['choices'][0]['message']['content'], historico
    
    except Exception as e:
        return f"Erro ao chamar API: {str(e)}", historico

# Rota para recomendar filmes, séries e animes (API FastAPI)
@app.post("/recomendar")
def recomendar(chat_request: ChatRequest):
    # Inicializa o histórico de conversa
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Obter resposta do assistente
    resposta_assistente, st.session_state["messages"] = chat_with_openai(
        chat_request.mensagem, 
        st.session_state["messages"]
    )
    
    return {"resposta": resposta_assistente}
