import requests
import streamlit as st

from api import BASE_URL
from modules.dashboard import modulo_dashboard
from modules.professores import modulo_professores
from modules.disciplinas import modulo_disciplinas
from modules.tarefas import modulo_tarefas
from modules.notas import modulo_notas
from styles import carregar_css
from modules.perfil import modulo_perfil

st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide"
)

carregar_css()


def tela_acesso():
    st.title("🎓 EduTrack AI")
    st.subheader("Portal Acadêmico Personalizado")

    tab_login, tab_cadastro = st.tabs(["Entrar", "Criar minha conta"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")

            if st.form_submit_button("Acessar meu painel"):
                resposta = requests.post(
                    f"{BASE_URL}/auth/login",
                    json={"email": email, "password": senha}
                )

                if resposta.status_code == 200:
                    dados = resposta.json()

                    token = (
                        dados.get("authToken")
                        or dados.get("auth_token")
                        or dados.get("token")
                    )

                    st.session_state.auth_token = token

                    usuario = requests.get(
                        f"{BASE_URL}/auth/me",
                        headers={
                            "Authorization": f"Bearer {token}"
                        }
                    )

                    if usuario.status_code == 200:
                        user_data = usuario.json()

                        st.session_state.user_id = user_data.get("id")
                        st.session_state.user_name = user_data.get("name", "")
                        st.session_state.user_email = user_data.get("email", "")

                    st.session_state.logged_in = True
                    st.success("Login realizado com sucesso!")
                    st.rerun()

                else:
                    st.error("Credenciais inválidas.")


    with tab_cadastro:
        with st.form("cadastro_form"):
            nome = st.text_input("Nome")
            email = st.text_input("E-mail para cadastro")
            senha = st.text_input("Senha para cadastro", type="password")

            if st.form_submit_button("Cadastrar"):
                resposta = requests.post(
                    f"{BASE_URL}/auth/signup",
                    json={"name": nome, "email": email, "password": senha}
                )

                if resposta.status_code in [200, 201]:
                    st.success("Conta criada! Agora faça login.")
                else:
                    st.error("Erro ao cadastrar usuário.")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    tela_acesso()
else:
    with st.sidebar:
        st.title("🎓 EduTrack AI")

        menu = st.radio(
            "Gerenciar:",
            [
                "Painel Geral",
                "Professores",
                "Disciplinas",
                "Tarefas",
                "Notas",
                "Perfil"
            ]
        )

        st.markdown("---")

        if st.button("Sair"):
            st.session_state.clear()
            st.rerun()

    if menu == "Painel Geral":
        modulo_dashboard()
    elif menu == "Professores":
        modulo_professores()
    elif menu == "Disciplinas":
        modulo_disciplinas()
    elif menu == "Tarefas":
        modulo_tarefas()
    elif menu == "Notas":
        modulo_notas()
    elif menu == "Perfil":
        modulo_perfil()