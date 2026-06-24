import streamlit as st

from services.api import api_delete_endpoint, api_get, api_patch_endpoint
from utils.api_ui import sucesso_ou_erro


def _carregar_usuario():
    usuario = api_get("auth/me", use_cache=False)
    if isinstance(usuario, dict):
        st.session_state.user_name = usuario.get("name") or st.session_state.get("user_name", "")
        st.session_state.user_email = usuario.get("email") or st.session_state.get("user_email", "")
        if usuario.get("id") is not None:
            st.session_state.user_id = usuario.get("id")


def modulo_perfil():
    st.header("Perfil")
    _carregar_usuario()

    nome_atual = st.session_state.get("user_name", "")
    email_atual = st.session_state.get("user_email", "")
    curso_atual = st.session_state.get("user_curso", "")
    semestre_atual = st.session_state.get("user_semestre", "")
    objetivo_atual = st.session_state.get("user_objetivo", "")
    lembretes_atual = st.session_state.get("user_lembretes", True)

    with st.container(border=True):
        st.subheader("Dados da conta")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Nome**")
            st.write(nome_atual or "Não informado")
            st.markdown("**Curso**")
            st.write(curso_atual or "Não informado")
            st.markdown("**Lembretes**")
            st.write("Ativados" if lembretes_atual else "Desativados")
        with col2:
            st.markdown("**E-mail**")
            st.write(email_atual or "Não informado")
            st.markdown("**Semestre**")
            st.write(semestre_atual or "Não informado")

    with st.container(border=True):
        st.subheader("Objetivo acadêmico")
        st.write(objetivo_atual or "Nenhum objetivo acadêmico cadastrado ainda.")

    with st.expander("Editar perfil", expanded=False):
        nome = st.text_input("Nome", value=nome_atual, placeholder="Digite seu nome")
        st.text_input("E-mail", value=email_atual, disabled=True)
        curso = st.text_input("Curso", value=curso_atual, placeholder="Ex.: Sistemas de Informação")
        opcoes_semestre = [
            "Selecione o semestre",
            "1º semestre",
            "2º semestre",
            "3º semestre",
            "4º semestre",
            "5º semestre",
            "6º semestre",
            "7º semestre",
            "8º semestre",
        ]
        semestre = st.selectbox(
            "Semestre",
            opcoes_semestre,
            index=opcoes_semestre.index(semestre_atual) if semestre_atual in opcoes_semestre else 0,
        )
        objetivo = st.text_area(
            "Objetivo acadêmico",
            value=objetivo_atual,
            placeholder="Ex.: melhorar minhas notas e organizar melhor meus prazos",
        )
        lembretes = st.checkbox("Receber lembretes de tarefas", value=lembretes_atual)
        st.caption(
            "Nome e e-mail são sincronizados com o Xano. Curso, semestre, objetivo e lembretes "
            "ficam salvos nesta sessão até existir tabela de perfil no backend."
        )

        if st.button("Salvar perfil"):
            resposta = api_patch_endpoint("auth/me", {"name": nome})
            if sucesso_ou_erro(resposta, sucesso="Perfil salvo com sucesso!", erro="Não foi possível salvar o perfil."):
                st.session_state.user_name = nome
                st.session_state.user_curso = curso
                st.session_state.user_semestre = semestre if semestre != "Selecione o semestre" else ""
                st.session_state.user_objetivo = objetivo
                st.session_state.user_lembretes = lembretes
                st.rerun()

    with st.expander("Excluir conta", expanded=False):
        st.warning("Sua conta será excluída permanentemente.")
        confirmar = st.text_input("Tem certeza? Digite EXCLUIR para confirmar")
        if st.button("Excluir minha conta", type="secondary", disabled=confirmar != "EXCLUIR"):
            resposta = api_delete_endpoint("auth/me")
            if sucesso_ou_erro(resposta, sucesso="Conta excluída.", erro="Não foi possível excluir sua conta."):
                st.session_state.clear()
                st.session_state.logged_in = False
                st.rerun()
