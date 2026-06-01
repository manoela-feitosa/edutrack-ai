import pandas as pd
import plotly.express as px
import streamlit as st

from api import api_get


def modulo_dashboard():
    nome_usuario = st.session_state.get("user_name", "estudante")

    st.markdown(f"""
    <h1 style='font-size:48px;'>Olá, {nome_usuario}!</h1>
    <p style='font-size:20px; color:#7C3AED;'>Que bom te ver de novo.</p>
    """, unsafe_allow_html=True)

    disciplinas = api_get("disciplinas")
    tarefas = api_get("tarefas")
    notas = [item for item in tarefas if item.get("nota") not in [None, ""]]

    total_disciplinas = len(disciplinas)
    total_tarefas = len(tarefas)
    media_geral = 0

    if notas:
        df_notas = pd.DataFrame(notas)
        if "nota" in df_notas.columns:
            df_notas["nota"] = pd.to_numeric(df_notas["nota"], errors="coerce")
            media_geral = round(df_notas["nota"].dropna().mean(), 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Disciplinas", total_disciplinas)
    col2.metric("Tarefas", total_tarefas)
    col3.metric("Média geral", media_geral)

    st.markdown("<br>", unsafe_allow_html=True)
    col_grafico, col_lista = st.columns([2, 1])

    with col_grafico:
        st.subheader("Desempenho acadêmico")
        if notas and disciplinas:
            df_notas = pd.DataFrame(notas)
            df_disciplinas = pd.DataFrame(disciplinas)
            df_plot = df_notas.merge(
                df_disciplinas,
                left_on="disc_id",
                right_on="id",
                suffixes=("_nota", "_disciplina"),
            )
            df_plot["nota"] = pd.to_numeric(df_plot["nota"], errors="coerce")
            df_plot = df_plot.dropna(subset=["nota"])
            candidatos_x = ["nome", "nome_tarefa", "titulo", "created_at_nota", "id_nota", "disc_id"]
            nome_coluna = next((col for col in candidatos_x if col in df_plot.columns), None)
            if nome_coluna is None or df_plot.empty:
                st.info("Cadastre notas para visualizar gráficos.")
            else:
                fig = px.line(df_plot, x=nome_coluna, y="nota", color="nome_disciplina", markers=True)
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#4C1D95"),
                    margin=dict(l=20, r=20, t=30, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Cadastre notas para visualizar gráficos.")

    with col_lista:
        st.subheader("Próximas tarefas")
        if tarefas:
            for tarefa in tarefas[:5]:
                nome = tarefa.get("nome_tarefa", "Tarefa")
                status = tarefa.get("status", "Pendente")
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.55); padding:16px; border-radius:18px; margin-bottom:12px; border:1px solid #F5D0FE;">
                    <b>{nome}</b><br>
                    <span style='color:#7C3AED'>{status}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma tarefa cadastrada.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Disciplinas")

    if disciplinas:
        cols = st.columns(2)
        for i, disc in enumerate(disciplinas):
            with cols[i % 2]:
                nome = disc.get("nome_disciplina", "Disciplina")
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.6); padding:22px; border-radius:24px; margin-bottom:18px; border:1px solid #F5D0FE; box-shadow:0 8px 24px rgba(168,85,247,0.08);">
                    <h4 style="color:#7C3AED; margin-bottom:8px;">{nome}</h4>
                    <p style="color:#6D28D9; margin:0;">Continue evoluindo.</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma disciplina cadastrada.")



