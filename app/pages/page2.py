import streamlit as st
import openai
import os
from dotenv import load_dotenv
from openai_agent2 import chat_with_openai  # Importa o agente correto
import time
import random

# Carregar variáveis do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Função wrapper para convocar a função com histórico
def get_chatgpt_response(prompt, conversation_history):
    try:
        response, updated_history  = chat_with_openai(prompt, conversation_history)
        return response
    except Exception as e:
        return f"Erro ao chamar o ChatGPT: {str(e)}"

# Interface no Streamlit
def main():
    st.title("Chat com JobGuru (Adivinhação de Profissão) :male_mage:")

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
            # Aguarda 3 segundos e reexecuta para esconder a mensagem
            time.sleep(3)
            st.session_state["show_api_message"] = False
            st.rerun()

    st.markdown("Este é o Assistente JobGuru <br> Com base em suas habilidades, interesses e até mesmo nos seus hobbies, este sábio assistente virtual analisará suas respostas e revelará qual carreira pode ser a ideal para você. <br> Desafie o Guru! Descreva um pouco sobre você e descubra sua vocação. :crystal_ball: :briefcase: ", unsafe_allow_html=True)

    # Sidebar indicando troca de páginas
    with st.sidebar:
        st.header("Menu")
        if st.button("Página Inicial"):
            st.switch_page("main_page.py")
        st.header("Assistentes")
        if st.button("Hitchcock :movie_camera:"):
            st.session_state["messages"] = []
            st.session_state["processing"] = False
            st.switch_page("pages/page1.py")
        if st.button("JobGuru :male_mage:"):
            st.switch_page("pages/page2.py")
        if st.button("Socratix :thinking_face:"):
            st.session_state["messages"] = []
            st.session_state["processing"] = False
            st.switch_page("pages/page3.py")

    # Inicializa o histórico de mensagens
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
        "Descreva um pouco sobre você e seus interesses... e eu revelarei a profissão que mais combina com a sua essência",
        "Conte-me suas habilidades, hobby ou rotina ... e eu usarei meu sexto sentido profissional para adivinhar sua função :crystal_ball:",
        "Quais são suas habilidades? O que te inspira? Me dê algumas pistas e eu desvendarei sua vocação!?"
    ]
    
    # Escolhe uma mensagem aleatória
    mensagem_selecionada = random.choice(mensagens_aleatorias)

    # Caixa de texto para entrada do usuário
    user_input = st.text_input("Conte-me suas habilidades, hobby ou rotina ... e eu usarei meu sexto sentido profissional para adivinhar sua função :crystal_ball:", key="user_input_page2", value="")

    # Botão para enviar a mensagem
    if st.button("Enviar :arrow_forward:", key="send_button"): 
    #and not st.session_state["processing"]:
        if user_input:
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
