import streamlit as st
import openai
import os
from dotenv import load_dotenv
from openai_agent import chat_with_openai

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurar a API Key
api_key = os.getenv("OPENAI_API_KEY")

# Função wrapper (opcional, para tratamento de erros) para chamar a função com o histórico
def get_chatgpt_response(prompt, conversation_history):
    try:
        response = chat_with_openai(prompt, conversation_history)  # Chama sua função diretamente, passando também o histórico
# Se a função retorna uma tupla (resposta, histórico), pega só a resposta
        if isinstance(response, tuple):
            return response[0]  # Assume que o primeiro elemento é a resposta
        return response  # Caso contrário, retorna diretamente
    except Exception as e:
        return f"Erro ao chamar o ChatGPT: {str(e)}"

# Interface no Streamlit
def main():
    st.title("Chat com Assistente 1")

    # Verificar se a chave foi carregada corretamente
    if api_key is None:
        st.markdown("<p style='color:red; font-style:italic;'>Erro: Não podemos prosseguir com a execução do programa. A chave da API não foi encontrada. Verifique o arquivo .env. ou contate o administrador do sistema.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:gray; font-style:italic;'>(API Key carregada com sucesso!)</p>", unsafe_allow_html=True)

    st.markdown("Este é o Assistente 1 <br> A sua especialidade é ...",unsafe_allow_html=True)

    # Inicializa o histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Exibe o histórico de mensagens
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Caixa de texto para entrada do usuário
    user_input = st.text_input("Bem-vindo ao Assistente da OpenAI!", key="user_input", value="")

    # Botão para enviar a mensagem
    if st.button("Enviar"):
        if user_input:
            # Adiciona a mensagem do usuário ao histórico
            if not st.session_state["messages"] or st.session_state["messages"][-1]["content"] != user_input:
                st.session_state["messages"].append({"role": "user", "content": user_input})

            # Chama a função com o prompt e o histórico
            response = get_chatgpt_response(user_input, st.session_state["messages"])

            # Adiciona a resposta ao histórico apenas se não for igual à última
            if not st.session_state["messages"] or st.session_state["messages"][-1]["content"] != response:
                st.session_state["messages"].append({"role": "assistant", "content": response})
            

            # Atualiza a interface
            st.rerun()
        else:
            st.warning("Por favor, digite uma mensagem antes de enviar.")

    # Opcional: botão para limpar o histórico
    if st.button("Limpar Histórico"):
        st.session_state["messages"] = []
        st.rerun()

if __name__ == "__main__":
    main()