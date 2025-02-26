import streamlit as st
import openai
import os
from dotenv import load_dotenv
from openai_agent import chat_with_openai

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurar a API Key
api_key = os.getenv("OPENAI_API_KEY")


# Interface no Streamlit
def main():
    st.title("Chat com Assistente 1")

    # Função wrapper (opcional, para tratamento de erros)
    def get_chatgpt_response(prompt):
        try:
            response = chat_with_openai(prompt)  # Chama sua função diretamente
            return response
        except Exception as e:
            return f"Erro ao chamar o ChatGPT: {str(e)}"

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
    user_input = st.text_input("Bem-vindo ao Assistente da OpenAI!", key="user_input")
    chat_with_openai(user_input)

    # Botão para enviar a mensagem
    if st.button("Enviar"):
        if user_input:
            # Adiciona a mensagem do usuário ao histórico
            st.session_state["messages"].append({"role": "user", "content": user_input})
            
            # Obtém a resposta da OpenAI
            response = chat_with_openai(user_input)
            
            # Adiciona a resposta ao histórico
            st.session_state["messages"].append({"role": "assistant", "content": response})
            
            # Força a reexecução para atualizar a interface
            st.rerun()
        else:
            st.warning("Por favor, digite uma mensagem antes de enviar.")

if __name__ == "__main__":
    main()




