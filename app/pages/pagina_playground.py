# pagina_playground.py
import streamlit as st
import openai
import os
from dotenv import load_dotenv
from firebase_init import db  # Importa o Firestore do firebase_init.py

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API da OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Função para criar um novo agente
def criar_agente(usuario_id, nome_agente, system_prompt):
    agente_ref = db.collection("agentes").document()
    agente_ref.set({
        "usuario_id": usuario_id,
        "nome_agente": nome_agente,
        "system_prompt": system_prompt,
        "historico": []
    })
    return agente_ref.id

def chat_com_agente(agente_id, mensagem):
    try:
        # Recupera o agente do Firestore
        agente_ref = db.collection("agentes").document(agente_id)
        agente = agente_ref.get()
        
        if not agente.exists:
            return "Agente não encontrado."
        
        agente_data = agente.to_dict()
        system_prompt = agente_data["system_prompt"]
        historico = agente_data.get("historico", [])  # Recupera o histórico ou inicializa como lista vazia
        
        # Adiciona o system_prompt ao histórico (se ainda não estiver presente)
        if not any(msg["role"] == "system" for msg in historico):
            historico.insert(0, {"role": "system", "content": system_prompt})
        
        # Adiciona a mensagem do usuário ao histórico
        historico.append({"role": "user", "content": mensagem})
        
        # Chama a API da OpenAI
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=historico
        )
        
        # Obtém a resposta do assistente
        resposta_assistente = resposta['choices'][0]['message']['content']
        
        # Adiciona a resposta ao histórico
        historico.append({"role": "assistant", "content": resposta_assistente})
        
        # Atualiza o histórico no Firestore
        agente_ref.update({"historico": historico})
        
        return resposta_assistente
    except Exception as e:
        print(f"Erro ao interagir com o agente: {e}")
        return f"Erro ao interagir com o agente: {str(e)}"

# Função para obter o histórico de conversas
def obter_historico(agente_id):
    agente_ref = db.collection("agentes").document(agente_id)
    agente = agente_ref.get()
    
    if not agente.exists:
        return None
    
    return agente.to_dict()["historico"]

# Interface para criar um novo agente
def interface_criar_agente():
    st.title("Criar Novo Agente")
    
    usuario_id = st.text_input("ID do Usuário", key="criar_usuario_id")
    nome_agente = st.text_input("Nome do Agente", key="criar_nome_agente")
    system_prompt = st.text_area("Prompt do Sistema", key="criar_system_prompt")
    
    if st.button("Criar Agente"):
        if usuario_id and nome_agente and system_prompt:
            agente_id = criar_agente(usuario_id, nome_agente, system_prompt)
            st.success(f"Agente criado com sucesso! ID: {agente_id}")
        else:
            st.error("Preencha todos os campos.")

# Interface para interagir com um agente
def interface_chat_agente():
    st.title("Chat com Agente")
    
    # Inicializa o histórico de mensagens e o estado de processamento
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "processing" not in st.session_state:
        st.session_state["processing"] = False

    # Exibe o histórico de mensagens
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada do usuário
    agente_id = st.text_input("ID do Agente", key="chat_agente_id")
    mensagem = st.text_input("Digite sua mensagem", key="chat_mensagem")
        
    if st.button("Enviar"):
        if agente_id and mensagem:
            # Adiciona a mensagem do usuário ao histórico
            st.session_state["messages"].append({"role": "user", "content": mensagem})
            
            # Chama a função para obter a resposta do assistente
            resposta = chat_com_agente(agente_id, mensagem)
            
            # Adiciona a resposta do assistente ao histórico
            st.session_state["messages"].append({"role": "assistant", "content": resposta})
            
            # Atualiza a interface
            st.rerun()
        else:
            st.error("Preencha o ID do agente e a mensagem.")
            
# Interface para visualizar o histórico de conversas
def interface_historico():
    st.title("Histórico de Conversas")
    
    agente_id = st.text_input("ID do Agente para ver o histórico", key="historico_agente_id")
    
    if st.button("Ver Histórico"):
        historico = obter_historico(agente_id)
        if historico:
            for msg in historico:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
        else:
            st.error("Agente não encontrado.")

# Menu principal
def main():
    st.sidebar.title("Menu")
    opcao = st.sidebar.selectbox("Escolha uma opção", ["Criar Agente", "Chat com Agente", "Histórico de Conversas"])
    
    if opcao == "Criar Agente":
        interface_criar_agente()
    elif opcao == "Chat com Agente":
        interface_chat_agente()
    elif opcao == "Histórico de Conversas":
        interface_historico()

if __name__ == "__main__":
    main()