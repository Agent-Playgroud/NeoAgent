# openai_agent2.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai  # Versão 0.28.0
import os
from dotenv import load_dotenv
import firebase_init  # Importa o módulo que inicializa o Firebase
from firebase_admin import firestore
import streamlit as st

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API da OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key  # Configuração para a versão 0.28.0

# Acessa o Firestore
db = firestore.client()

# Função para interagir com o ChatGPT
def chat_with_openai(prompt, conversation_history, usuario_id, agente_id):
    """Interage com a OpenAI para obter respostas."""
    try:
        # Define o system_prompt (contexto do assistente)
        system_prompt = (
            "Você é um assistente que adivinha a profissão do usuário. Faça perguntas relevantes "
            "para adivinhar qual é a profissão da pessoa. Use as respostas para ajustar as perguntas subsequentes."
        )

        # Adiciona o system_prompt ao histórico de conversa (se ainda não estiver presente)
        if not any(msg["role"] == "system" for msg in conversation_history):
            conversation_history.insert(0, {"role": "system", "content": system_prompt})

        # Adiciona o prompt do usuário ao histórico de conversa
        conversation_history.append({"role": "user", "content": prompt})
        
        # Chama a API da OpenAI (versão 0.28.0)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        
        # Obtém a resposta do assistente
        resposta_assistente = response['choices'][0]['message']['content']
        
        # Adiciona a resposta ao histórico de conversa
        conversation_history.append({"role": "assistant", "content": resposta_assistente})
        
        # Salva o histórico no Firestore
        save_chat_history(usuario_id, prompt, resposta_assistente, agente_id)
        
        return resposta_assistente, conversation_history
    except Exception as e:
        return f"Erro ao chamar o ChatGPT: {str(e)}", conversation_history

# Função para salvar o histórico de conversa no Firestore
def save_chat_history(usuario_id, mensagem, resposta, agente_id):
    try:
        # Referência para a coleção de histórico de conversas do Agente 2
        historico_ref = db.collection(f'conversas_{agente_id}')

        # Adiciona a mensagem do usuário
        historico_ref.add({
            'usuario_id': usuario_id,
            'agente_id': agente_id,
            'mensagem': mensagem,
            'remetente': 'user',
            'data_envio': firestore.SERVER_TIMESTAMP
        })

        # Adiciona a resposta do assistente
        historico_ref.add({
            'usuario_id': usuario_id,
            'agente_id': agente_id,
            'mensagem': resposta,
            'remetente': 'assistant',
            'data_envio': firestore.SERVER_TIMESTAMP
        })

        print(f"Histórico salvo com sucesso para o agente {agente_id}.")
    except Exception as e:
        print(f'Erro ao salvar histórico: {e}')

# Inicializar FastAPI
app = FastAPI()

# Modelo de dados para a requisição
class ChatRequest(BaseModel):
    usuario_id: str
    mensagem: str
    agente_id: str

# Rota para interagir com o ChatGPT
@app.post("/chat")
def chat(chat_request: ChatRequest):
    try:
        # Recupera o histórico do Firestore
        historico_ref = db.collection(f'conversas_{chat_request.agente_id}').order_by("data_envio").stream()
        historico = [{"role": doc.to_dict()["remetente"], "content": doc.to_dict()["mensagem"]} for doc in historico_ref]

        # Chama a função para interagir com o ChatGPT
        resposta_assistente, historico = chat_with_openai(
            chat_request.mensagem, 
            historico,
            chat_request.usuario_id,
            chat_request.agente_id
        )
        
        return {"resposta": resposta_assistente}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao interagir com o agente: {str(e)}")

# Função principal para executar o FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)