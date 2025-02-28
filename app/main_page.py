import streamlit as st
import requests
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os
import files_bd
import user_bd
import agent_bd

# Configurações do Google OAuth
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
REDIRECT_URI = "http://localhost:8501"  # Para testes locais
CLIENT_SECRETS_FILE = "client_secret.json"  # Arquivo baixado do Google Cloud

# Função para carregar ou criar credenciais
def get_credentials():
    if "credentials" not in st.session_state:
        st.session_state["credentials"] = None
    return st.session_state["credentials"]

# Fluxo de autenticação
def authenticate():
    if not get_credentials():
        # Só cria o fluxo se o usuário ainda não estiver autenticado
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )
        # Armazena o state no session_state
        st.session_state["state"] = state
        st.markdown(
            f"""
            <a href="{authorization_url}" target="_self">Para acessar é necessário fazer login com o Google. Clique aqui para ser redirecionado.</a>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("Autenticação já realizada.")

# Processa o callback do Google
def process_callback():
    if "code" in st.query_params:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
            state=st.session_state.get("state")  # Usa o state armazenado, se existir
        )
        try:
            # Troca o código por um token
            flow.fetch_token(code=st.query_params["code"])
            st.session_state["credentials"] = flow.credentials
            st.session_state.pop("state", None)  # Remove o state após uso
            st.query_params.clear()  # Limpa os parâmetros da URL
            st.rerun()  # Reexecuta o script
        except Exception as e:
            st.error(f"Erro ao processar o callback: {str(e)}")
            st.session_state.pop("state", None)  # Limpa o state em caso de erro
    elif "state" in st.query_params and "state" not in st.session_state:
        st.error("Estado inválido ou ausente. Tente fazer login novamente.")

# Obtém informações do usuário
def get_user_info(credentials):
    if credentials:
        try:
            headers = {"Authorization": f"Bearer {credentials.token}"}
            response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Erro ao obter user_info: {str(e)}")
            return None
    return None

# Aplicação principal
def main():
    st.title("Neoagent")


    # Processa o callback primeiro
    process_callback()

    # Verifica as credenciais e exibe o conteúdo
    credentials = get_credentials()
    if credentials:
        user_info = get_user_info(credentials)
        if user_info:
            st.write("Bem-vindo(a),", user_info["name"])
            st.write("Você está logado como:", user_info["email"])
            st.write("Selecione abaixo o assistente que deseja consultar")

            if "page" in st.session_state:
                st.session_state.pop("page", None)  # Remove a navegação automática
            
            col1, col2, col3 = st.columns(3)
            
            # Botões indicando troca de páginas
            with col1:
                if st.button("Hitchcock :movie_camera:"):
                    st.switch_page("pages/page1.py")
                
            with col2:
                if st.button("JobGuru :male_mage:"):
                    st.switch_page("pages/page2.py")

            with col3:
                if st.button("Socratix :thinking_face:"):
                    st.switch_page("pages/page3.py")
            
            #verifica se o usuario esta cadastrado no banco de dados
            # if functions_bd.localizar_usuario(user_info["email"]) == []:
            #     try:
            #         user = functions_bd.dados_user(user_info["given_name"], user_info["family_name"], user_info["email"])
            #         user.cadastrar_usuario()
            #     except:
            #         try:
            #             user = functions_bd.dados_user(user_info["given_name"],'NaN', user_info["email"])
            #             user.cadastrar_usuario()
            #         except:
            #             user = functions_bd.dados_user(user_info["name"],'NaN', user_info["email"])
            #             user.cadastrar_usuario()
            # else:
            #     pass
            if st.button("Logout"):
                st.session_state["credentials"] = None
                st.session_state.pop("state", None)
                st.rerun()
        else:
            st.error("Não foi possível obter as informações do usuário.")
    else:
        authenticate()

if __name__ == "__main__":
    main()

