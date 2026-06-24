from datetime import date, datetime

import pandas as pd
import streamlit as st

from services.api import api_delete, api_get, api_patch, api_post
from utils.api_ui import sucesso_ou_erro


def _valor(item, *nomes, padrao=""):
    for nome in nomes:
        if nome in item and item.get(nome) not in [None, ""]:
            return item.get(nome)
    return padrao


def _tipo(item):
    return str(_valor(item, "tipo", "Tipo", padrao="tarefa")).strip().lower()


def _formatar_data(valor):
    if not valor:
        return ""
    texto = str(valor)[:10]
    if "-" in texto:
        partes = texto.split("-")
        if len(partes) == 3:
            return f"{partes[2]}/{partes[1]}/{partes[0]}"
    return texto


def _parse_data(valor):
    if not valor:
        return date.today()
    texto = str(valor)[:10]
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            pass
    return date.today()


def _normalizar_notas(registros, disciplinas):
    mapa_disciplinas = {disc.get("id"): disc.get("nome_disciplina", "Disciplina") for disc in disciplinas}
    linhas = []
    for item in registros:
        if _tipo(item) != "nota":
            continue
        nota = _valor(item, "nota", padrao=None)
        if nota in [None, ""]:
            continue
        disc_id = _valor(item, "disc_id", "disciplina_id", "disciplinas_id", padrao=None)
        linhas.append(
            {
                "Código": _valor(item, "id", "task_id", "tarefas_id", padrao="-"),
                "Atividade": _valor(item, "nome_tarefa", "nome", "atividade", "titulo", padrao="Avaliação"),
                "disc_id": disc_id,
                "Disciplina": mapa_disciplinas.get(disc_id, _valor(item, "disciplina", "nome_disciplina", padrao="Não informada")),
                "Nota": nota,
                "Data": _formatar_data(_valor(item, "data", "data_avaliacao", "created_at", padrao="")),
            }
        )
    return pd.DataFrame(linhas, columns=["Código", "Atividade", "disc_id", "Disciplina", "Nota", "Data"])


def _opcoes_por_id(itens, campo_nome):
    return {
        f"{item.get(campo_nome, 'Sem nome')} (#{item.get('id')})": item.get("id")
        for item in itens
        if item.get("id") is not None
    }


def modulo_notas():
    st.header("Notas")

    disciplinas = api_get("disciplinas")
    if disciplinas is None:
        return
    if not disciplinas:
        st.warning("Cadastre uma disciplina primeiro.")
        return

    opcoes_disciplinas = _opcoes_por_id(disciplinas, "nome_disciplina")

    with st.expander("Lançar nota", expanded=True):
        nome = st.text_input("Nome da atividade/avaliação")
        disciplina_escolhida = st.selectbox(
            "Disciplina",
            options=list(opcoes_disciplinas.keys()),
            key="nota_nova_disciplina",
        )
        nota = st.number_input("Nota", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        data_avaliacao = st.date_input("Data da avaliação", value=date.today(), format="DD/MM/YYYY")

        if st.button("Salvar nota"):
            if not nome:
                st.warning("Preencha o nome da atividade ou avaliação.")
                return
            resposta = api_post(
                "tarefas",
                {
                    "tipo": "nota",
                    "nome": nome,
                    "nome_tarefa": nome,
                    "disc_id": opcoes_disciplinas[disciplina_escolhida],
                    "nota": nota,
                    "data": data_avaliacao.isoformat(),
                },
            )
            if sucesso_ou_erro(resposta, sucesso="Nota cadastrada!", erro="Não foi possível cadastrar a nota."):
                st.rerun()

    registros = api_get("tarefas")
    if registros is None:
        return
    df = _normalizar_notas(registros, disciplinas)
    if df.empty:
        st.info("Nenhuma nota cadastrada ainda.")
        return

    st.subheader("Notas cadastradas")
    st.dataframe(df.drop(columns=["disc_id"]), use_container_width=True, hide_index=True)

    with st.expander("Editar ou excluir nota", expanded=False):
        opcoes_notas = {
            f"{linha['Atividade']} - {linha['Disciplina']} (#{linha['Código']})": linha
            for _, linha in df.iterrows()
            if linha["Código"] != "-"
        }
        if not opcoes_notas:
            st.info("Nenhuma nota com código válido para editar ou excluir.")
            return

        escolha = st.selectbox(
            "Selecione a nota",
            list(opcoes_notas.keys()),
            key="nota_editar_item",
        )
        selecionada = opcoes_notas[escolha]
        nota_id = selecionada["Código"]

        nome_edit = st.text_input("Atividade", value=selecionada["Atividade"])
        nomes_disciplinas = list(opcoes_disciplinas.keys())
        disciplina_indice = 0
        for i, nome_disc in enumerate(nomes_disciplinas):
            if opcoes_disciplinas[nome_disc] == selecionada["disc_id"]:
                disciplina_indice = i
                break
        disciplina_edit = st.selectbox(
            "Disciplina",
            nomes_disciplinas,
            index=disciplina_indice,
            key="nota_editar_disciplina",
        )
        nota_edit = st.number_input("Nota", min_value=0.0, max_value=10.0, value=float(selecionada["Nota"]), step=0.1)
        data_edit = st.date_input("Data da avaliação", value=_parse_data(selecionada["Data"]), format="DD/MM/YYYY")
        confirmar_exclusao = st.checkbox("Confirmar exclusão da nota selecionada")

        col_salvar, _, col_excluir = st.columns([1, 2, 1])
        with col_salvar:
            salvar = st.button("Salvar alterações", key="salvar_nota")
        with col_excluir:
            excluir = st.button(
                "Excluir nota",
                type="secondary",
                disabled=not confirmar_exclusao,
                key="excluir_nota",
            )

        if salvar:
            resposta = api_patch(
                "tarefas",
                nota_id,
                {
                    "tipo": "nota",
                    "nome": nome_edit,
                    "nome_tarefa": nome_edit,
                    "disc_id": opcoes_disciplinas[disciplina_edit],
                    "nota": nota_edit,
                    "data": data_edit.isoformat(),
                },
            )
            if sucesso_ou_erro(resposta, sucesso="Nota atualizada!", erro="Não foi possível atualizar a nota."):
                st.rerun()

        if excluir:
            resposta = api_delete("tarefas", nota_id)
            if sucesso_ou_erro(resposta, sucesso="Nota excluída!", erro="Não foi possível excluir a nota."):
                st.rerun()
