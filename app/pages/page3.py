import streamlit as st
import os
from dotenv import load_dotenv
from openai_agent3 import chat_with_openai  # Corrigido para a função correta

# Carregar variáveis do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Função para chamar o assistente correto
def get_chatgpt_response(prompt, conversation_history, usuario_id, agente_id):
    try:
        # Chama a função do agente que agora salva no banco de dados
        response, conversation_history = chat_with_openai(prompt, conversation_history, usuario_id, agente_id)
        
        # Exibir mensagem de sucesso
        st.success("Mensagem e histórico salvos com sucesso no banco de dados.")
        return response, conversation_history
    
    except Exception as e:
        # Exibir mensagem de erro
        st.error(f"Erro ao salvar no banco de dados: {str(e)}")
        return f"Erro ao chamar o ChatGPT: {str(e)}", conversation_history

# Interface no Streamlit
def main():
    st.title("Chat com Assistente 3 (Filosofia e a Arte de pensar)")

    if api_key is None:
        st.error("Erro: A chave da API não foi encontrada.")
        return

    # ID do usuário e do agente para salvar no banco
    usuario_id = "usuario_teste"  # Isso pode vir de um sistema de login real
    agente_id = "3"  # ID do agente

    if "messages_page3" not in st.session_state:
        st.session_state["messages_page3"] = []

    # Exibir mensagens no chat
    for message in st.session_state["messages_page3"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada do usuário
    user_input = st.text_input("Digite sua resposta ou pergunta:", key="user_input_page3")

    if st.button("Enviar"):
        if user_input:
            st.session_state["messages_page3"].append({"role": "user", "content": user_input})
            response, st.session_state["messages_page3"] = get_chatgpt_response(user_input, st.session_state["messages_page3"], usuario_id, agente_id)
            st.session_state["messages_page3"].append({"role": "assistant", "content": response})
            st.rerun()
        else:
            st.warning("Digite uma mensagem antes de enviar.")

    # Limpar histórico
    if st.button("Limpar Histórico"):
        st.session_state["messages_page3"] = []
        st.rerun()

if __name__ == "__main__":
    main()
