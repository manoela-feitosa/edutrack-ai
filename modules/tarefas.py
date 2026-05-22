import pandas as pd
import streamlit as st

from api import api_get, api_post


def modulo_tarefas():
    st.header("📝 Tarefas")

    disciplinas = api_get("disciplinas")

    if not disciplinas:
        st.warning("Cadastre uma disciplina primeiro.")
        return

    opcoes_disciplinas = {
        disc["nome_disciplina"]: disc["id"]
        for disc in disciplinas
    }

    with st.expander("➕ Nova Tarefa", expanded=True):
        nome = st.text_input("Nome da Tarefa")

        disciplina_escolhida = st.selectbox(
            "Disciplina",
            options=list(opcoes_disciplinas.keys())
        )

        status = st.selectbox(
            "Status",
            ["Pendente", "Em andamento", "Concluída"]
        )

        if st.button("Salvar Tarefa"):
            resposta = api_post(
                "tarefas",
                {
                    "nome_tarefa": nome,
                    "disc_id": opcoes_disciplinas[disciplina_escolhida],
                    "status": status
                }
            )

            if resposta.status_code in [200, 201]:
                st.success("Tarefa cadastrada!")
                st.rerun()
            else:
                st.error("Erro ao cadastrar tarefa.")
                st.write(resposta.text)

    tarefas = api_get("tarefas")

    if tarefas:
        st.subheader("Tarefas cadastradas")

        df = pd.DataFrame(tarefas)

        mapa_disciplinas = {
            disc["id"]: disc["nome_disciplina"]
            for disc in disciplinas
        }

        df["Disciplina"] = df["disc_id"].map(mapa_disciplinas)

        df = df.rename(columns={
            "id": "Código",
            "nome_tarefa": "Tarefa",
            "status": "Status"
        })

        st.dataframe(
            df[["Código", "Tarefa", "Disciplina", "Status"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhuma tarefa cadastrada ainda.")