import requests
import streamlit as st

from api import BASE_URL
from modules.dashboard import modulo_dashboard
from modules.professores import modulo_professores
from modules.disciplinas import modulo_disciplinas
from modules.tarefas import modulo_tarefas
from modules.notas import modulo_notas
from modules.perfil import modulo_perfil
from modules.automacoes import modulo_automacoes
from styles import TEMAS, carregar_css


st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "tema_visual_v2" not in st.session_state:
    st.session_state.tema_visual_v2 = "Rosé"

tema_escolhido = st.sidebar.selectbox(
    "Tema",
    list(TEMAS.keys()),
    index=list(TEMAS.keys()).index(st.session_state.tema_visual_v2),
    key="tema_visual_v2",
)

carregar_css(tema_escolhido)


def tela_acesso():
    col_esq, col_dir = st.columns([1.05, 0.95])

    with col_esq:
        st.markdown('<div class="hero-login">', unsafe_allow_html=True)
        st.markdown(
            '<div class="logo-login">EduTrack <span>AI</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <h1>Seu semestre sob<br><span>Controle</span></h1>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <p>
                Planeje seus estudos,
                acompanhe suas tarefas
                e alcance seus objetivos.
            </p>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                """
                <div class="beneficio-card">
                    <div class="beneficio-icone">OK</div>
                    <b>Seguro</b>
                    <small>Seus dados<br>protegidos</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                """
                <div class="beneficio-card">
                    <div class="beneficio-icone">AI</div>
                    <b>Inteligente</b>
                    <small>IA para apoiar<br>seus estudos</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                """
                <div class="beneficio-card">
                    <div class="beneficio-icone">ID</div>
                    <b>Personalizado</b>
                    <small>Feito para<br>sua rotina</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_dir:
        tab_login, tab_cadastro = st.tabs(["Entrar", "Criar minha conta"])

        with tab_login:
            st.markdown(
                """
                <h2 style="color:#311942;">
                    Bem-vindo de volta!
                </h2>
                <p style="color:#cf3aed;">
                    Entre na sua conta para continuar sua jornada.
                </p>
                """,
                unsafe_allow_html=True,
            )

            with st.form("login_form"):
                email = st.text_input("E-mail", placeholder="seu@email.com")
                senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

                if st.form_submit_button("Acessar meu painel"):
                    resposta = requests.post(
                        f"{BASE_URL}/auth/login",
                        json={"email": email, "password": senha},
                    )

                    if resposta.status_code == 200:
                        dados = resposta.json()
                        token = dados.get("authToken") or dados.get("auth_token") or dados.get("token")

                        if not token:
                            st.error("A API respondeu, mas não retornou token.")
                            st.write(dados)
                            st.stop()

                        st.session_state.auth_token = token
                        usuario = requests.get(
                            f"{BASE_URL}/auth/me",
                            headers={"Authorization": f"Bearer {token}"},
                        )

                        if usuario.status_code == 200:
                            user_data = usuario.json()
                            st.session_state.user_id = user_data.get("id")
                            st.session_state.user_name = (
                                user_data.get("name")
                                or user_data.get("nome")
                                or email.split("@")[0]
                            )
                            st.session_state.user_email = user_data.get("email", email)

                        st.session_state.logged_in = True
                        st.success("Login realizado com sucesso!")
                        st.rerun()

                    else:
                        st.error("Credenciais inválidas ou erro na API.")
                        st.write("Status:", resposta.status_code)
                        st.write("Resposta da API:", resposta.text)

        with tab_cadastro:
            st.markdown(
                """
                <h2 style="color:#311942;">
                    Crie sua conta!
                </h2>
                <p style="color:#cf3aed;">
                    Junte-se a nós e transforme sua jornada acadêmica.
                </p>
                """,
                unsafe_allow_html=True,
            )

            with st.form("cadastro_form"):
                nome = st.text_input("Nome")
                email = st.text_input("E-mail para cadastro")
                senha = st.text_input("Senha para cadastro", type="password")

                if st.form_submit_button("Criar conta"):
                    resposta = requests.post(
                        f"{BASE_URL}/auth/signup",
                        json={"name": nome, "email": email, "password": senha},
                    )

                    if resposta.status_code in [200, 201]:
                        st.success("Conta criada com sucesso! Agora faça login.")
                    else:
                        st.error("Erro ao cadastrar usuário.")
                        st.write("Status:", resposta.status_code)
                        st.write("Resposta da API:", resposta.text)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    tela_acesso()
else:
    with st.sidebar:
        st.title("EduTrack AI")
        menu = st.radio(
            "Gerenciar:",
            [
                "Painel Geral",
                "Professores",
                "Disciplinas",
                "Tarefas",
                "Notas",
                "Central de Rotina",
                "Perfil",
            ],
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
    elif menu == "Central de Rotina":
        modulo_automacoes()
    elif menu == "Perfil":
        modulo_perfil()



