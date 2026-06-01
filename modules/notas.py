from datetime import date

import pandas as pd
import streamlit as st

from api import api_delete, api_get, api_patch, api_post


def _valor(item, *nomes, padrao=""):
    for nome in nomes:
        if nome in item and item.get(nome) not in [None, ""]:
            return item.get(nome)
    return padrao


def _formatar_data(valor):
    if not valor:
        return ""
    texto = str(valor)[:10]
    if "-" in texto:
        partes = texto.split("-")
        if len(partes) == 3:
            return f"{partes[2]}/{partes[1]}/{partes[0]}"
    return texto


def _normalizar_notas(registros, disciplinas):
    mapa_disciplinas = {disc.get("id"): disc.get("nome_disciplina", "Disciplina") for disc in disciplinas}
    linhas = []
    for item in registros:
        nota = _valor(item, "nota", padrao=None)
        if nota in [None, ""]:
            continue
        disc_id = _valor(item, "disc_id", "disciplina_id", "disciplinas_id", padrao=None)
        linhas.append(
            {
                "Código": _valor(item, "id", "task_id", "tarefas_id", padrao="-"),
                "Atividade": _valor(item, "nome", "nome_tarefa", "atividade", "titulo", padrao="Avaliação"),
                "Disciplina": mapa_disciplinas.get(disc_id, _valor(item, "disciplina", "nome_disciplina", padrao="Não informada")),
                "Nota": nota,
                "Data": _formatar_data(_valor(item, "data", "data_avaliacao", "created_at", padrao="")),
            }
        )
    return pd.DataFrame(linhas, columns=["Código", "Atividade", "Disciplina", "Nota", "Data"])


def modulo_notas():
    st.header("Notas")

    disciplinas = api_get("disciplinas")
    if not disciplinas:
        st.warning("Cadastre uma disciplina primeiro.")
        return

    opcoes_disciplinas = {disc.get("nome_disciplina", "Disciplina"): disc.get("id") for disc in disciplinas if disc.get("id") is not None}

    with st.expander("Lançar nota", expanded=True):
        nome = st.text_input("Nome da atividade/avaliação")
        disciplina_escolhida = st.selectbox("Disciplina", options=list(opcoes_disciplinas.keys()))
        nota = st.number_input("Nota", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        data_avaliacao = st.date_input("Data da avaliação", value=date.today(), format="DD/MM/YYYY")

        if st.button("Salvar nota"):
            if not nome:
                st.warning("Preencha o nome da atividade ou avaliação.")
                return
            resposta = api_post(
                "tarefas",
                {
                    "nome": nome,
                    "nome_tarefa": nome,
                    "disc_id": opcoes_disciplinas[disciplina_escolhida],
                    "nota": nota,
                    "data": data_avaliacao.isoformat(),
                },
            )
            if resposta and resposta.status_code in [200, 201]:
                st.success("Nota cadastrada!")
                st.rerun()
            else:
                st.error("Erro ao cadastrar nota.")
                if resposta:
                    st.write(resposta.text)

    registros = api_get("tarefas")
    df = _normalizar_notas(registros, disciplinas)
    if df.empty:
        st.info("Nenhuma nota cadastrada ainda.")
        return

    st.subheader("Notas cadastradas")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Editar ou excluir nota")
    opcoes_notas = {f"{linha['Atividade']} - {linha['Disciplina']} (#{linha['Código']})": linha for _, linha in df.iterrows() if linha["Código"] != "-"}
    if not opcoes_notas:
        st.info("Nenhuma nota com código válido para editar ou excluir.")
        return

    escolha = st.selectbox("Selecione a nota", list(opcoes_notas.keys()))
    selecionada = opcoes_notas[escolha]
    nota_id = selecionada["Código"]

    with st.form("editar_nota_form"):
        nome_edit = st.text_input("Atividade", value=selecionada["Atividade"])
        disciplina_edit = st.selectbox("Disciplina", list(opcoes_disciplinas.keys()))
        nota_edit = st.number_input("Nota", min_value=0.0, max_value=10.0, value=float(selecionada["Nota"]), step=0.1)
        data_edit = st.date_input("Data da avaliação", value=date.today(), format="DD/MM/YYYY")
        salvar = st.form_submit_button("Salvar alterações")

    if salvar:
        resposta = api_patch(
            "tarefas",
            nota_id,
            {
                "nome": nome_edit,
                "nome_tarefa": nome_edit,
                "disc_id": opcoes_disciplinas[disciplina_edit],
                "nota": nota_edit,
                "data": data_edit.isoformat(),
            },
        )
        if resposta and resposta.status_code in [200, 201]:
            st.success("Nota atualizada!")
            st.rerun()
        else:
            st.error("Erro ao atualizar nota.")
            if resposta:
                st.write(resposta.text)

    if st.button("Excluir nota", type="secondary"):
        resposta = api_delete("tarefas", nota_id)
        if resposta and resposta.status_code in [200, 204]:
            st.success("Nota excluída!")
            st.rerun()
        else:
            st.error("Erro ao excluir nota.")
            if resposta:
                st.write(resposta.text)
