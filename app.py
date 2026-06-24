import base64
from pathlib import Path

import requests
import streamlit as st

from services.api import BASE_URL, mensagem_erro
from modules.dashboard import modulo_dashboard
from modules.professores import modulo_professores
from modules.disciplinas import modulo_disciplinas
from modules.tarefas import modulo_tarefas
from modules.notas import modulo_notas
from modules.perfil import modulo_perfil
from modules.automacoes import modulo_automacoes
from utils.styles import TEMAS, carregar_css

REQUEST_TIMEOUT = 10
DEFAULT_THEME = "Algodão Doce"
THEME_VERSION = "login-default-theme-v1"
ASSETS_DIR = Path(__file__).parent / "assets"


def _asset_data_uri(nome_arquivo):
    caminho = ASSETS_DIR / nome_arquivo
    if not caminho.exists():
        return ""
    return f"data:image/png;base64,{base64.b64encode(caminho.read_bytes()).decode('ascii')}"


def _render_post_login_ambient():
    space_src = _asset_data_uri("space-bg.png")
    if space_src:
        st.markdown(f'<img class="app-ambient-bg" src="{space_src}" alt="">', unsafe_allow_html=True)


def _iniciais(nome):
    partes = [parte for parte in str(nome).split() if parte]
    if not partes:
        return "E"
    return "".join(parte[0] for parte in partes[:2]).upper()


st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Garante que o Streamlit saiba se o usuario ja esta autenticado.
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Define e valida o tema visual usado na interface.
opcoes_tema = list(TEMAS.keys())
tema_padrao = DEFAULT_THEME if DEFAULT_THEME in opcoes_tema else opcoes_tema[0]

# Atualiza o tema quando ha mudanca de versao visual do app.
if st.session_state.get("tema_visual_version") != THEME_VERSION:
    st.session_state.tema_visual_v2 = tema_padrao
    st.session_state.tema_visual_version = THEME_VERSION

if "tema_visual_v2" not in st.session_state:
    st.session_state.tema_visual_v2 = tema_padrao

tema_atual = st.session_state.get("tema_visual_v2", tema_padrao)
if tema_atual not in opcoes_tema:
    tema_atual = tema_padrao
    st.session_state.tema_visual_v2 = tema_atual

if st.session_state.logged_in:
    # Depois do login, o tema atual e aplicado e o seletor aparece no menu lateral.
    tema_escolhido = tema_atual
else:
    # Antes do login, a tela inicial usa sempre o tema padrao claro.
    tema_escolhido = tema_padrao

carregar_css(tema_escolhido)


def tela_acesso():
    # Renderiza a tela publica de login, cadastro e recuperacao de senha.
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
                    <div class="beneficio-icone">🛡️</div>
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
                    <div class="beneficio-icone">🧠</div>
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
                    <div class="beneficio-icone">👤</div>
                    <b>Personalizado</b>
                    <small>Feito para<br>sua rotina</small>
                </div>
                """,
                unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_dir:
        mostrar_recuperacao = st.query_params.get("recuperar_senha") == "1"
        tab_login, tab_cadastro = st.tabs(["Entrar", "Criar minha conta"])

        with tab_login:
            if mostrar_recuperacao:
                st.markdown(
                    """
                    <h2 style="color:var(--primary);">
                        Alterar senha
                    </h2>
                    <p style="color:var(--muted);">
                        Informe seu e-mail para receber o link de recuperação.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

                with st.form("recuperar_senha_form"):
                    email_recuperacao = st.text_input(
                        "E-mail da conta",
                        placeholder="seu@email.com",
                    )

                    if st.form_submit_button("Enviar link de recuperação"):
                        try:
                            resposta = requests.get(
                                f"{BASE_URL}/reset/request-reset-link",
                                params={"email": email_recuperacao},
                                timeout=REQUEST_TIMEOUT,
                            )
                        except requests.RequestException:
                            st.error("Não foi possível enviar o link agora. Tente novamente em instantes.")
                            st.stop()

                        if resposta.status_code == 200:
                            st.success("Se o e-mail estiver cadastrado, você receberá o link de recuperação.")
                        else:
                            st.error("Não foi possível enviar o link. Verifique o e-mail e tente novamente.")

                st.markdown(
                    '<a class="forgot-password-link" href="/">Voltar para o login</a>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <h2 style="color:var(--primary);">
                        Bem-vindo de volta!
                    </h2>
                    <p style="color:var(--muted);">
                        Entre na sua conta para continuar sua jornada.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

                with st.form("login_form"):
                    email = st.text_input("E-mail", placeholder="seu@email.com")
                    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

                    col_acessar, col_esqueci = st.columns([1, 1])
                    with col_acessar:
                        acessar_painel = st.form_submit_button("Acessar meu painel")
                    with col_esqueci:
                        st.markdown(
                            '<a class="forgot-password-link forgot-password-inline" href="/?recuperar_senha=1">Esqueceu a senha?</a>',
                            unsafe_allow_html=True,
                        )

                    if acessar_painel:
                        try:
                            resposta = requests.post(
                                f"{BASE_URL}/auth/login",
                                json={"email": email, "password": senha},
                                timeout=REQUEST_TIMEOUT,
                            )
                        except requests.RequestException:
                            st.error("Não foi possível entrar agora. Tente novamente em instantes.")
                            st.stop()

                        if resposta.status_code == 200:
                            dados = resposta.json()
                            token = dados.get("authToken") or dados.get("auth_token") or dados.get("token")

                            if not token:
                                st.error("Não foi possível concluir o login. Tente novamente.")
                                st.stop()

                            st.session_state.auth_token = token
                            try:
                                usuario = requests.get(
                                    f"{BASE_URL}/auth/me",
                                    headers={"Authorization": f"Bearer {token}"},
                                    timeout=REQUEST_TIMEOUT,
                                )
                            except requests.RequestException:
                                st.error("Não foi possível carregar seus dados. Tente novamente.")
                                st.stop()

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
                            if resposta.status_code == 429:
                                st.error(mensagem_erro(resposta, "Limite de requisições do Xano atingido."))
                            else:
                                st.error("E-mail ou senha inválidos.")

        with tab_cadastro:
            st.markdown(
                """
                <h2 style="color:var(--primary);">
                    Crie sua conta!
                </h2>
                <p style="color:var(--muted);">
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
                    try:
                        resposta = requests.post(
                            f"{BASE_URL}/auth/signup",
                            json={"name": nome, "email": email, "password": senha},
                            timeout=REQUEST_TIMEOUT,
                        )
                    except requests.RequestException:
                        st.error("Não foi possível criar a conta agora. Tente novamente em instantes.")
                        st.stop()

                    if resposta.status_code in [200, 201]:
                        st.success("Conta criada com sucesso! Agora faça login.")
                    elif resposta.status_code == 429:
                        st.error(mensagem_erro(resposta, "Limite de requisições do Xano atingido."))
                    else:
                        st.error(mensagem_erro(resposta, "Não foi possível criar a conta. Verifique os dados e tente novamente."))


if not st.session_state.logged_in:
    tela_acesso()
else:
    _render_post_login_ambient()
    with st.sidebar:
        nome_usuario = st.session_state.get("user_name") or "Estudante"
        email_usuario = st.session_state.get("user_email") or "Conta conectada"
        iniciais_usuario = _iniciais(nome_usuario)

        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="brand-mark">🎓</span>
                <div>
                    <div class="sidebar-brand-title">EduTrack <span>AI</span></div>
                    <div class="muted sidebar-brand-subtitle">Academic Platform</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="sidebar-user-card">
                <span class="avatar">{iniciais_usuario}</span>
                <div>
                    <strong>{nome_usuario}</strong>
                    <small>{email_usuario}</small>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="theme-picker-label">Tema</div>', unsafe_allow_html=True)
        st.selectbox(
            "Tema",
            opcoes_tema,
            index=opcoes_tema.index(tema_atual),
            key="tema_visual_v2",
            label_visibility="collapsed",
        )

        menu = st.radio(
            "Navegação",
            [
                "Painel Geral",
                "Professores",
                "Disciplinas",
                "Tarefas",
                "Notas",
                "Central de Rotina",
                "Perfil",
            ],
            label_visibility="collapsed",
        )

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        if st.button("Sair da conta"):
            tema_atual = st.session_state.get("tema_visual_v2", DEFAULT_THEME)
            versao_tema = st.session_state.get("tema_visual_version", THEME_VERSION)
            st.session_state.clear()
            st.session_state.tema_visual_v2 = tema_atual
            st.session_state.tema_visual_version = versao_tema
            st.session_state.logged_in = False
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



