import pandas as pd
import streamlit as st

from services.api import api_delete, api_get, api_patch, api_post
from utils.api_ui import sucesso_ou_erro


def _valor(item, nome, padrao=""):
    valor = item.get(nome)
    return valor if valor not in [None, ""] else padrao


def modulo_professores():
    st.header("Professores")

    with st.expander("Adicionar professor", expanded=True):
        nome = st.text_input("Nome do professor")
        email = st.text_input("E-mail de contato")

        if st.button("Cadastrar professor"):
            if not nome or not email:
                st.warning("Preencha o nome e o e-mail do professor.")
                return

            resposta = api_post("professores", {"nome": nome, "email": email})
            if sucesso_ou_erro(resposta, sucesso="Professor cadastrado!", erro="Não foi possível cadastrar o professor."):
                st.rerun()

    dados = api_get("professores")
    if dados is None:
        return
    if not dados:
        st.info("Nenhum professor cadastrado ainda.")
        return

    st.subheader("Professores cadastrados")
    df = pd.DataFrame(dados).rename(columns={"id": "Código", "nome": "Professor", "email": "E-mail"})
    st.dataframe(df[["Código", "Professor", "E-mail"]], use_container_width=True, hide_index=True)

    with st.expander("Editar ou excluir professor", expanded=False):
        professores_com_id = [prof for prof in dados if prof.get("id") is not None]
        opcoes_professores = {
            f"{_valor(prof, 'nome', 'Professor')} (#{prof.get('id')})": prof
            for prof in professores_com_id
        }

        if not opcoes_professores:
            st.info("Nenhum professor com código válido para editar ou excluir.")
            return

        escolha = st.selectbox(
            "Selecione o professor",
            list(opcoes_professores.keys()),
            key="professor_editar_item",
        )
        professor = opcoes_professores[escolha]
        professor_id = professor["id"]

        nome_edit = st.text_input("Nome", value=_valor(professor, "nome"))
        email_edit = st.text_input("E-mail", value=_valor(professor, "email"))
        confirmar_exclusao = st.checkbox("Confirmar exclusão do professor selecionado")

        col_salvar, _, col_excluir = st.columns([1, 2, 1])
        with col_salvar:
            salvar = st.button("Salvar alterações", key="salvar_professor")
        with col_excluir:
            excluir = st.button(
                "Excluir professor",
                type="secondary",
                disabled=not confirmar_exclusao,
                key="excluir_professor",
            )

        if salvar:
            if not nome_edit or not email_edit:
                st.warning("Preencha o nome e o e-mail do professor.")
                return
            resposta = api_patch("professores", professor_id, {"nome": nome_edit, "email": email_edit})
            if sucesso_ou_erro(resposta, sucesso="Professor atualizado!", erro="Não foi possível atualizar o professor."):
                st.rerun()

        if excluir:
            resposta = api_delete("professores", professor_id)
            if sucesso_ou_erro(resposta, sucesso="Professor excluído!", erro="Não foi possível excluir o professor."):
                st.rerun()
