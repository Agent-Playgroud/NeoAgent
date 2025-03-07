# -*- coding: utf-8 -*- 
from fastapi import FastAPI
from pydantic import BaseModel
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
def get_chatgpt_response(prompt, conversation_history):
    """Função para interagir com a API da OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history + [{"role": "user", "content": prompt}]
        )
        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        return response['choices'][0]['message']['content'], conversation_history
    except Exception as e:
        return f"Erro ao chamar API: {str(e)}", conversation_history

# Rota para recomendar filmes
@app.post("/recomendar")
def recomendar(chat_request: ChatRequest):
    # Inicializa o histórico de conversa
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    # Obter resposta do assistente
    resposta_assistente, st.session_state["messages"] = get_chatgpt_response(chat_request.mensagem, st.session_state["messages"])
    
    return {"resposta": resposta_assistente}

