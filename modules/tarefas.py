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


def _filtrar_tarefas(registros):
    return [item for item in registros if _tipo(item) != "nota"]


def _formatar_data(valor):
    if not valor:
        return "—"
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


def _normalizar_tarefas(tarefas, disciplinas):
    mapa_disciplinas = {disc.get("id"): disc.get("nome_disciplina", "Disciplina") for disc in disciplinas}
    linhas = []
    for tarefa in tarefas:
        disc_id = _valor(tarefa, "disc_id", "disciplina_id", "disciplinas_id", padrao=None)
        linhas.append(
            {
                "Código": _valor(tarefa, "id", "task_id", "tarefas_id", padrao="-"),
                "Tarefa": _valor(tarefa, "nome_tarefa", "tarefa", "nome", "titulo", padrao="Tarefa sem título"),
                "Disciplina": mapa_disciplinas.get(disc_id, _valor(tarefa, "disciplina", "nome_disciplina", padrao="Não informada")),
                "Prazo": _formatar_data(_valor(tarefa, "data", "prazo", padrao="")),
                "Status": _valor(tarefa, "status", padrao="Pendente"),
            }
        )
    return pd.DataFrame(linhas, columns=["Código", "Tarefa", "Disciplina", "Prazo", "Status"])


def _opcoes_por_id(itens, campo_nome):
    return {
        f"{item.get(campo_nome, 'Sem nome')} (#{item.get('id')})": item.get("id")
        for item in itens
        if item.get("id") is not None
    }


def modulo_tarefas():
    st.header("Tarefas")

    disciplinas = api_get("disciplinas")
    if disciplinas is None:
        return
    if not disciplinas:
        st.warning("Cadastre uma disciplina primeiro.")
        return

    opcoes_disciplinas = _opcoes_por_id(disciplinas, "nome_disciplina")

    with st.expander("Nova tarefa", expanded=True):
        nome = st.text_input("Nome da tarefa")
        disciplina_escolhida = st.selectbox(
            "Disciplina",
            options=list(opcoes_disciplinas.keys()),
            key="tarefa_nova_disciplina",
        )
        prazo = st.date_input("Prazo", value=date.today(), format="DD/MM/YYYY")
        status = st.selectbox(
            "Status",
            ["Pendente", "Em andamento", "Concluída"],
            key="tarefa_nova_status",
        )

        if st.button("Salvar tarefa"):
            if not nome:
                st.warning("Preencha o nome da tarefa.")
                return
            resposta = api_post(
                "tarefas",
                {
                    "tipo": "tarefa",
                    "nome_tarefa": nome,
                    "nome": nome,
                    "disc_id": opcoes_disciplinas[disciplina_escolhida],
                    "status": status,
                    "data": prazo.isoformat(),
                },
            )
            if sucesso_ou_erro(resposta, sucesso="Tarefa cadastrada!", erro="Não foi possível cadastrar a tarefa."):
                st.rerun()

    registros_tarefas = api_get("tarefas")
    if registros_tarefas is None:
        return
    tarefas = _filtrar_tarefas(registros_tarefas)
    if not tarefas:
        st.info("Nenhuma tarefa cadastrada ainda.")
        return

    st.subheader("Tarefas cadastradas")
    st.dataframe(_normalizar_tarefas(tarefas, disciplinas), use_container_width=True, hide_index=True)

    with st.expander("Editar ou excluir tarefa", expanded=False):
        tarefas_com_id = [t for t in tarefas if _valor(t, "id", "task_id", "tarefas_id", padrao=None) not in [None, "-"]]
        if not tarefas_com_id:
            st.info("Nenhuma tarefa com código válido para editar ou excluir.")
            return

        opcoes_tarefas = {
            f"{_valor(t, 'nome_tarefa', 'tarefa', 'nome', 'titulo', padrao='Tarefa sem título')} (#{_valor(t, 'id', 'task_id', 'tarefas_id')})": t
            for t in tarefas_com_id
        }
        escolha = st.selectbox(
            "Selecione a tarefa",
            list(opcoes_tarefas.keys()),
            key="tarefa_editar_item",
        )
        tarefa = opcoes_tarefas[escolha]
        tarefa_id = _valor(tarefa, "id", "task_id", "tarefas_id")

        nome_edit = st.text_input("Tarefa", value=_valor(tarefa, "nome_tarefa", "tarefa", "nome", "titulo", padrao=""))
        disc_atual = _valor(tarefa, "disc_id", "disciplina_id", "disciplinas_id", padrao=None)
        nomes = list(opcoes_disciplinas.keys())
        indice = 0
        for i, nome_disc in enumerate(nomes):
            if opcoes_disciplinas[nome_disc] == disc_atual:
                indice = i
                break
        disciplina_edit = st.selectbox(
            "Disciplina",
            nomes,
            index=indice,
            key="tarefa_editar_disciplina",
        )
        prazo_edit = st.date_input(
            "Prazo",
            value=_parse_data(_valor(tarefa, "data", "prazo", padrao="")),
            format="DD/MM/YYYY",
            key="tarefa_editar_prazo",
        )
        status_opcoes = ["Pendente", "Em andamento", "Concluída"]
        status_atual = _valor(tarefa, "status", padrao="Pendente")
        status_indice = status_opcoes.index(status_atual) if status_atual in status_opcoes else 0
        status_edit = st.selectbox(
            "Status",
            status_opcoes,
            index=status_indice,
            key="tarefa_editar_status",
        )
        confirmar_exclusao = st.checkbox("Confirmar exclusão da tarefa selecionada")

        col_salvar, _, col_excluir = st.columns([1, 2, 1])
        with col_salvar:
            salvar = st.button("Salvar alterações", key="salvar_tarefa")
        with col_excluir:
            excluir = st.button(
                "Excluir tarefa",
                type="secondary",
                disabled=not confirmar_exclusao,
                key="excluir_tarefa",
            )

        if salvar:
            resposta = api_patch(
                "tarefas",
                tarefa_id,
                {
                    "tipo": "tarefa",
                    "nome_tarefa": nome_edit,
                    "nome": nome_edit,
                    "disc_id": opcoes_disciplinas[disciplina_edit],
                    "status": status_edit,
                    "data": prazo_edit.isoformat(),
                },
            )
            if sucesso_ou_erro(resposta, sucesso="Tarefa atualizada!", erro="Não foi possível atualizar a tarefa."):
                st.rerun()

        if excluir:
            resposta = api_delete("tarefas", tarefa_id)
            if sucesso_ou_erro(resposta, sucesso="Tarefa excluída!", erro="Não foi possível excluir a tarefa."):
                st.rerun()
