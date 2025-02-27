import streamlit as st
import openai
import os
from dotenv import load_dotenv
from openai_agent import chat_with_openai
import time

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurar a API Key
api_key = os.getenv("OPENAI_API_KEY")

# Função wrapper para chamar a função com o histórico
def get_chatgpt_response(prompt, conversation_history):
    try:
        response, updated_history = chat_with_openai(prompt, conversation_history)
        return response
    except Exception as e:
        return f"Erro ao chamar o ChatGPT: {str(e)}"

# Interface no Streamlit
def main():
    st.title("Chat com Assistente 1")

    # Inicializa o estado para controlar a mensagem temporária
    if "show_api_message" not in st.session_state:
        st.session_state["show_api_message"] = None

    # Verificar se a chave foi carregada corretamente
    if api_key is None:
        st.markdown("<p style='color:red; font-style:italic;'> :coffin: Erro: Não podemos prosseguir com a execução do programa. A chave da API não foi encontrada. Verifique o arquivo .env ou contate o administrador do sistema.</p>", unsafe_allow_html=True)
        return
    else:
        # Mostra a mensagem de sucesso apenas se ainda não foi exibida
        if st.session_state["show_api_message"] is None:
            st.markdown("<p style='color:gray; font-style:italic;'>(API Key carregada com sucesso!)</p>", unsafe_allow_html=True)
            st.session_state["show_api_message"] = True
            # Aguarda 3 segundos e reexecuta para esconder a mensagem
            time.sleep(3)
            st.session_state["show_api_message"] = False
            st.rerun()

    st.markdown("Este é o Assistente 1 <br> Caso precise de recomendações, tenha dúvidas, ou queira apenas bater um papo sobre o universo do cinema. <br> Este é o lugar correto para isso", unsafe_allow_html=True)

    # Sidebar indicando troca de páginas
    with st.sidebar:
        st.header("Menu")
        if st.button("Página Inicial", key="nav_home"):
            st.switch_page("main_page.py")
        st.header("Assistentes")
        if st.button("Assistente 1", key="nav_assist1"):
            st.switch_page("pages/page1.py")
        if st.button("Assistente 2", key="nav_assist2"):
            st.switch_page("pages/page2.py")

    # Inicializa o histórico de mensagens e controle de envio
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "processing" not in st.session_state:
        st.session_state["processing"] = False

    # Exibe o histórico de mensagens
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Caixa de texto para entrada do usuário
    user_input = st.text_input("Como posso ajudar?", key="user_input", value="")

    # Botão para enviar a mensagem
    if st.button("Enviar :arrow_forward:", key="send_button") and not st.session_state["processing"]:
        if user_input:
            st.session_state["processing"] = True
            response = get_chatgpt_response(user_input, st.session_state["messages"])
            st.session_state["processing"] = False
            st.rerun()
        else:
            st.warning("Por favor, digite uma mensagem antes de enviar.")

    # Botão para limpar o histórico
    if st.button("Limpar Histórico :wastebasket:", key="clear_button"):
        st.session_state["messages"] = []
        st.session_state["processing"] = False
        st.rerun()

if __name__ == "__main__":
    main()




