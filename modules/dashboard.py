import pandas as pd
import plotly.express as px
import streamlit as st

from api import api_get


def modulo_dashboard():
    st.header("📊 Painel Geral")

    professores = api_get("professores")
    disciplinas = api_get("disciplinas")
    tarefas = api_get("tarefas")

    col1, col2, col3 = st.columns(3)
    col1.metric("Professores", len(professores))
    col2.metric("Disciplinas", len(disciplinas))
    col3.metric("Tarefas", len(tarefas))

    st.markdown("---")

    if tarefas and disciplinas:
        df_tarefas = pd.DataFrame(tarefas)
        df_disciplinas = pd.DataFrame(disciplinas)

        df_plot = df_tarefas.merge(
            df_disciplinas,
            left_on="disc_id",
            right_on="id",
            suffixes=("_tarefa", "_disciplina")
        )

        if "nota" in df_plot.columns:
            fig = px.bar(
                df_plot,
                x="nome_tarefa" if "nome_tarefa" in df_plot.columns else "nome",
                y="nota",
                color="nome_disciplina" if "nome_disciplina" in df_plot.columns else None,
                title="Notas por Disciplina",
                text_auto=True
            )

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Cadastre dados para visualizar o dashboard.")