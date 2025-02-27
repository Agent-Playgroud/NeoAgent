import streamlit as st
import openai
import os
from dotenv import load_dotenv
from openai_agent3 import chat_with_openai  # Importa o agente correto

# Carregar variáveis do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Função para chamar o assistente correto
def get_chatgpt_response(prompt, conversation_history):
    try:
        response = chat_with_openai(prompt, conversation_history)
        if isinstance(response, tuple):
            return response[0]
        return response
    except Exception as e:
        return f"Erro ao chamar o ChatGPT: {str(e)}"

# Interface no Streamlit
def main():
    st.title("Chat com Assistente 3 (Filosifia e a Arte de pensar)")

    if api_key is None:
        st.error("Erro: A chave da API não foi encontrada.")
        return

    if "messages_page3" not in st.session_state:
        st.session_state["messages_page3"] = []

    for message in st.session_state["messages_page3"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.text_input("Digite sua resposta ou pergunta:", key="user_input_page2")

    if st.button("Enviar"):
        if user_input:
            st.session_state["messages_page3"].append({"role": "user", "content": user_input})
            response = get_chatgpt_response(user_input, st.session_state["messages_page3"])
            st.session_state["messages_page3"].append({"role": "assistant", "content": response})
            st.rerun()
        else:
            st.warning("Digite uma mensagem antes de enviar.")

    if st.button("Limpar Histórico"):
        st.session_state["messages_page3"] = []
        st.rerun()

if __name__ == "__main__":
    main()
