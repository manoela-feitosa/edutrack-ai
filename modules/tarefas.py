import pandas as pd
import streamlit as st

from api import api_delete, api_get, api_patch, api_post


def _valor(item, *nomes, padrao=""):
    for nome in nomes:
        if nome in item and item.get(nome) not in [None, ""]:
            return item.get(nome)
    return padrao


def _filtrar_tarefas(registros):
    return [
        item
        for item in registros
        if item.get("tipo", "tarefa") != "nota"
    ]


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
                "Status": _valor(tarefa, "status", padrao="Pendente"),
            }
        )
    return pd.DataFrame(linhas, columns=["Código", "Tarefa", "Disciplina", "Status"])


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
        disciplina_escolhida = st.selectbox("Disciplina", options=list(opcoes_disciplinas.keys()))
        status = st.selectbox("Status", ["Pendente", "Em andamento", "Concluída"])

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
                },
            )
            if resposta is not None and resposta.status_code in [200, 201]:
                st.success("Tarefa cadastrada!")
                st.rerun()
            else:
                st.error("Não foi possível cadastrar a tarefa. Verifique os dados e tente novamente.")

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
        escolha = st.selectbox("Selecione a tarefa", list(opcoes_tarefas.keys()))
        tarefa = opcoes_tarefas[escolha]
        tarefa_id = _valor(tarefa, "id", "task_id", "tarefas_id")

        with st.form("editar_tarefa_form"):
            nome_edit = st.text_input("Tarefa", value=_valor(tarefa, "nome_tarefa", "tarefa", "nome", "titulo", padrao=""))
            disc_atual = _valor(tarefa, "disc_id", "disciplina_id", "disciplinas_id", padrao=None)
            nomes = list(opcoes_disciplinas.keys())
            indice = 0
            for i, nome_disc in enumerate(nomes):
                if opcoes_disciplinas[nome_disc] == disc_atual:
                    indice = i
                    break
            disciplina_edit = st.selectbox("Disciplina", nomes, index=indice)
            status_opcoes = ["Pendente", "Em andamento", "Concluída"]
            status_atual = _valor(tarefa, "status", padrao="Pendente")
            status_indice = status_opcoes.index(status_atual) if status_atual in status_opcoes else 0
            status_edit = st.selectbox("Status", status_opcoes, index=status_indice)
            col_salvar, col_excluir = st.columns(2)
            with col_salvar:
                salvar = st.form_submit_button("Salvar alterações")
            with col_excluir:
                excluir = st.form_submit_button("Excluir tarefa", type="secondary")

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
                },
            )
            if resposta is not None and resposta.status_code in [200, 201]:
                st.success("Tarefa atualizada!")
                st.rerun()
            else:
                st.error("Não foi possível atualizar a tarefa. Tente novamente.")

        if excluir:
            resposta = api_delete("tarefas", tarefa_id)
            if resposta is not None and resposta.status_code in [200, 204]:
                st.success("Tarefa excluída!")
                st.rerun()
            else:
                st.error("Não foi possível excluir a tarefa. Tente novamente.")
