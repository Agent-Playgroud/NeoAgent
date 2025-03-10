import streamlit as st
import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import json
import os

# Configurações do Google OAuth
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
REDIRECT_URI = "http://localhost:8501"  # Para testes locais
CLIENT_SECRETS_FILE = "google_credentials.json"  # Arquivo baixado do Google Cloud

# Função para carregar ou criar credenciais
def get_credentials():  
    if "credentials" not in st.session_state:
        st.session_state["credentials"] = None
    return st.session_state["credentials"]

# Fluxo de autenticação
def authenticate():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    # Se não há credenciais, inicia o fluxo de autenticação
    if not get_credentials():
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )
        st.session_state["state"] = state
        st.write("Prossiga com o login com o Google para acessar a aplicação:	")
        st.markdown(f":key: [Login com o Google]({authorization_url})")
    else:
        st.write("Você já está autenticado!")

# Callback para processar o código retornado pelo Google
def process_callback():
    if "code" in st.query_params and "state" in st.session_state:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
            state=st.session_state["state"]
        )
        flow.fetch_token(code=st.query_params["code"])
        st.session_state["credentials"] = flow.credentials
        st.query_params.clear()  # Limpa os parâmetros da URL
        st.rerun()

# Obter informações do usuário
def get_user_info(credentials):
    if credentials:
        headers = {"Authorization": f"Bearer {credentials.token}"}
        response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
        return response.json()
    return None

# Aplicação principal
def main():
    st.title("NeoAgent - Portal de Acesso")

    # Processa o callback se houver um código na URL
    process_callback()

    # Verifica as credenciais
    credentials = get_credentials()
    if not credentials:
        authenticate()
    else:
        user_info = get_user_info(credentials)
        if user_info:
            st.write("Bem-vindo(a),", user_info["name"])
            st.write("E-mail:", user_info["email"])
            if st.button("Logout"):
                st.session_state["credentials"] = None
                st.rerun()
        else:
            st.error("Erro ao obter informações do usuário.")

if __name__ == "__main__":
    main()

st.sidebar.title("NeoAgent - Portal de Acesso")
with st.sidebar:
    st.header("Menu")
    if st.button("Tela Inicial"):
        st.switch_page("g4_assistant.py")
    st.header("Assistentes")
    if st.button("Assistente 1"):
        st.switch_page("pages/page1.py")
    if st.button("Assistente 2"):
        st.switch_page("pages/page2.py")




