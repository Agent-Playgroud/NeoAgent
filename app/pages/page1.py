import streamlit as st
import openai
import os
from dotenv import load_dotenv
from openai_agent import chat_with_openai
import time
import random

# Carregar variáveis do arquivo .env e Configura a API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Função wrapper para convocar a função com histórico
def get_chatgpt_response(prompt, conversation_history):
    try:
        response, updated_history = chat_with_openai(prompt, conversation_history)
        return response
    except Exception as e:
        return f"Erro ao chamar o ChatGPT: {str(e)}"

# Interface no Streamlit
def main():
    st.title("Chat com Hitchcock :movie_camera:")

    # Inicializa o estado para controlar a mensagem temporária
    if "show_api_message" not in st.session_state:
        st.session_state["show_api_message"] = None

    # Verifica se a chave foi carregada corretamente
    if api_key is None:
        st.markdown("<p style='color:red; font-style:italic;'> :coffin: Erro: Não podemos prosseguir com a execução do programa. A chave da API não foi encontrada. Verifique o arquivo .env ou contate o administrador do sistema.</p>", unsafe_allow_html=True)
        return
    else:
        # Mostra a mensagem de sucesso apenas se ainda não foi exibida
        if st.session_state["show_api_message"] is None:
            st.markdown("<p style='color:gray; font-style:italic;'>(:white_check_mark: API Key carregada com sucesso!)</p>", unsafe_allow_html=True)
            st.session_state["show_api_message"] = True
            # Aguarda 1 segundos e reexecuta para esconder a mensagem
            time.sleep(1)
            st.session_state["show_api_message"] = False
            st.rerun()

    st.markdown("Este é o Assistente Hitchcock <br> Caso precise de recomendações, tenha dúvidas, ou queira apenas bater um papo sobre o universo do cinema, basta iniciar a conversa", unsafe_allow_html=True)

    # Sidebar indicando troca de páginas
    with st.sidebar:
        st.header("Menu")
        if st.button("Página Inicial", key="nav_home"):
            st.switch_page("main_page.py")
        st.header("Assistentes")
        if st.button("Hitchcock :movie_camera:", key="nav_assist1"):
            st.switch_page("pages/page1.py")
        if st.button("JobGuru :male_mage:", key="nav_assist2"):
            st.session_state["messages"] = []
            st.session_state["processing"] = False
            st.switch_page("pages/page2.py")
        if st.button("Socratix :thinking_face:", key="nav_assist3"):
            st.session_state["messages"] = []
            st.session_state["processing"] = False
            st.switch_page("pages/page3.py")

    # Inicializa o histórico de mensagens e controle de envio
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "processing" not in st.session_state:
        st.session_state["processing"] = False

    # Exibe o histórico de mensagens
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Lista de mensagens aleatórias
    mensagens_aleatorias = [
        "Diga algo misterioso, como se fosse um roteiro de suspense...",
        "Peça uma lista dos melhores filmes de terror trash para assistir numa sexta-feira 13 :zombie:",
        "Você está diante de um mestre da cinematografia. Qual é a sua dúvida?"
    ]

    # Escolhe uma mensagem aleatória
    mensagem_selecionada = random.choice(mensagens_aleatorias)

    # Caixa de texto para entrada do usuário
    user_input = st.text_input("Você está diante de um mestre da cinematografia. Qual é a sua dúvida?", key="user_input")

    # Botão para enviar a mensagem
    if st.button("Enviar :arrow_forward:", key="send_button") and not st.session_state["processing"]:
        if user_input.strip():  # Usa strip() para remover espaços em branco
            st.session_state["processing"] = True
            response = get_chatgpt_response(user_input, st.session_state["messages"])
            st.session_state["processing"] = False
            st.rerun()
        else:
            st.warning("Vamos lá! Digite alguma mensagem antes de enviar.")

    # Botão para limpar o histórico
    if st.button("Limpar Histórico :wastebasket:", key="clear_button"):
        st.session_state["messages"] = []
        st.session_state["processing"] = False
        st.rerun()

if __name__ == "__main__":
    main()