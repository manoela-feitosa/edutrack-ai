import pandas as pd
import streamlit as st

from services.api import api_delete, api_get, api_patch, api_post
from utils.api_ui import sucesso_ou_erro


def _valor(item, nome, padrao=""):
    valor = item.get(nome)
    return valor if valor not in [None, ""] else padrao


def _opcoes_professores(professores):
    return {
        f"{prof.get('nome', 'Professor')} (#{prof.get('id')})": prof.get("id")
        for prof in professores
        if prof.get("id") is not None
    }


def modulo_disciplinas():
    st.header("Disciplinas")

    professores = api_get("professores")
    if professores is None:
        return
    if not professores:
        st.warning("Cadastre um professor antes de criar disciplinas.")
        return

    opcoes_professores = _opcoes_professores(professores)

    with st.expander("Nova disciplina", expanded=True):
        nome = st.text_input("Nome da disciplina")
        professor_escolhido = st.selectbox(
            "Professor responsável",
            options=list(opcoes_professores.keys()),
            key="disciplina_novo_professor",
        )

        if st.button("Salvar disciplina"):
            if not nome:
                st.warning("Preencha o nome da disciplina.")
                return

            resposta = api_post("disciplinas", {"nome_disciplina": nome, "prof_id": opcoes_professores[professor_escolhido]})
            if sucesso_ou_erro(resposta, sucesso="Disciplina cadastrada!", erro="Não foi possível cadastrar a disciplina."):
                st.rerun()

    disciplinas = api_get("disciplinas")
    if disciplinas is None:
        return
    if not disciplinas:
        st.info("Nenhuma disciplina cadastrada ainda.")
        return

    st.subheader("Disciplinas cadastradas")
    df = pd.DataFrame(disciplinas)
    mapa_professores = {prof["id"]: prof["nome"] for prof in professores}
    df["Professor"] = df["prof_id"].map(mapa_professores).fillna("Não informado")
    df = df.rename(columns={"id": "Código", "nome_disciplina": "Disciplina"})
    st.dataframe(df[["Código", "Disciplina", "Professor"]], use_container_width=True, hide_index=True)

    with st.expander("Editar ou excluir disciplina", expanded=False):
        disciplinas_com_id = [disc for disc in disciplinas if disc.get("id") is not None]
        opcoes_disciplinas = {
            f"{_valor(disc, 'nome_disciplina', 'Disciplina')} (#{disc.get('id')})": disc
            for disc in disciplinas_com_id
        }

        if not opcoes_disciplinas:
            st.info("Nenhuma disciplina com código válido para editar ou excluir.")
            return

        escolha = st.selectbox(
            "Selecione a disciplina",
            list(opcoes_disciplinas.keys()),
            key="disciplina_editar_item",
        )
        disciplina = opcoes_disciplinas[escolha]
        disciplina_id = disciplina["id"]

        nome_edit = st.text_input("Disciplina", value=_valor(disciplina, "nome_disciplina"))
        nomes_professores = list(opcoes_professores.keys())
        prof_atual = disciplina.get("prof_id")
        prof_indice = 0
        for i, nome_prof in enumerate(nomes_professores):
            if opcoes_professores[nome_prof] == prof_atual:
                prof_indice = i
                break
        professor_edit = st.selectbox(
            "Professor responsável",
            nomes_professores,
            index=prof_indice,
            key="disciplina_editar_professor",
        )
        confirmar_exclusao = st.checkbox("Confirmar exclusão da disciplina selecionada")

        col_salvar, _, col_excluir = st.columns([1, 2, 1])
        with col_salvar:
            salvar = st.button("Salvar alterações", key="salvar_disciplina")
        with col_excluir:
            excluir = st.button(
                "Excluir disciplina",
                type="secondary",
                disabled=not confirmar_exclusao,
                key="excluir_disciplina",
            )

        if salvar:
            if not nome_edit:
                st.warning("Preencha o nome da disciplina.")
                return
            resposta = api_patch(
                "disciplinas",
                disciplina_id,
                {"nome_disciplina": nome_edit, "prof_id": opcoes_professores[professor_edit]},
            )
            if sucesso_ou_erro(resposta, sucesso="Disciplina atualizada!", erro="Não foi possível atualizar a disciplina."):
                st.rerun()

        if excluir:
            resposta = api_delete("disciplinas", disciplina_id)
            if sucesso_ou_erro(resposta, sucesso="Disciplina excluída!", erro="Não foi possível excluir a disciplina."):
                st.rerun()
