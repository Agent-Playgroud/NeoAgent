# openai_agent3.py
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
            "Você é um filósofo. Quando um usuário fizer uma pergunta, você nunca responderá diretamente, "
            "apenas dará uma resposta na forma de uma pergunta. Seu objetivo é estimular o pensamento."
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
        # Referência para a coleção de histórico de conversas do Agente 3
        historico_ref = db.collection(f'conversas_{agente_id}')  # A coleção é agora específica para o agente

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
    # Inicializa o histórico de conversa
    if "messages_agent3" not in st.session_state:
        st.session_state["messages_agent3"] = []

    # Obter resposta do assistente
    resposta_assistente, st.session_state["messages_agent3"] = chat_with_openai(
        chat_request.mensagem, 
        st.session_state["messages_agent3"],
        chat_request.usuario_id,
        chat_request.agente_id
    )
    
    return {"resposta": resposta_assistente}

# Função principal para executar o Streamlit
def main():
    """
    Função principal para a interface do Streamlit.
    """
    st.title("Agente Três - Filosofia e a Arte de Pensar")
    
    # Verifica se a chave da API foi configurada
    if openai_api_key is None:
        st.error("Erro: A chave da API da OpenAI não foi encontrada.")
        return

    # Inicializa o histórico de mensagens (se não existir)
    if "messages_agent3" not in st.session_state:
        st.session_state["messages_agent3"] = []

    # IDs de usuário e agente (esses valores podem vir de uma autenticação ou configuração)
    usuario_id = "usuario_teste"  # Exemplo: ajustar conforme o caso
    agente_id = "agente_3"        # Exemplo: ajustar conforme o caso

    # Exibe as mensagens anteriores
    for message in st.session_state["messages_agent3"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto do usuário
    user_input = st.text_input("Digite sua resposta ou pergunta:", key="user_input_agent3")

    # Botão para enviar a mensagem
    if st.button("Enviar"):
        if user_input:
            # Adiciona a mensagem do usuário ao histórico
            st.session_state["messages_agent3"].append({"role": "user", "content": user_input})
            
            # Chama a função para obter a resposta do assistente
            resposta_assistente, st.session_state["messages_agent3"] = chat_with_openai(
                user_input, 
                st.session_state["messages_agent3"],
                usuario_id,
                agente_id
            )
            
            # Adiciona a resposta do assistente ao histórico
            st.session_state["messages_agent3"].append({"role": "assistant", "content": resposta_assistente})
            
            # Atualiza a interface
            st.rerun()
        else:
            st.warning("Digite uma mensagem antes de enviar.")

    # Botão para limpar o histórico
    if st.button("Limpar Histórico"):
        st.session_state["messages_agent3"] = []
        st.rerun()

if __name__ == "__main__":
    main()