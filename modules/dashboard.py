from html import escape
import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from services.api import api_get

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"


def _asset_data_uri(nome_arquivo):
    caminho = ASSETS_DIR / nome_arquivo
    if not caminho.exists():
        return ""
    return f"data:image/png;base64,{base64.b64encode(caminho.read_bytes()).decode('ascii')}"


def _tipo(item):
    return str(item.get("tipo") or item.get("Tipo") or "tarefa").strip().lower()


def _eh_nota(item):
    return _tipo(item) == "nota"


def _eh_tarefa(item):
    return _tipo(item) != "nota"


def modulo_dashboard():
    nome_usuario = escape(st.session_state.get("user_name", "estudante"))
    books_src = _asset_data_uri("books-left.png")

    st.markdown(
        f"""
        <div class="dashboard-hero">
            <div class="pill">EduTrack AI</div>
            <h2>Olá, {nome_usuario}!</h2>
            <p>
                Seu plano de estudos em um painel visual, organizado e pronto
                para acompanhar disciplinas, tarefas e desempenho acadêmico.
            </p>
            <div class="hero-kpis">
                <div class="mini-stat"><b>Foco</b><span>rotina de estudos</span></div>
                <div class="mini-stat"><b>Notas</b><span>desempenho acadêmico</span></div>
                <div class="mini-stat"><b>Tarefas</b><span>entregas e prazos</span></div>
            </div>
            {'<img class="hero-books" src="' + books_src + '" alt="Materiais de estudo">' if books_src else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

    disciplinas = api_get("disciplinas")
    registros = api_get("tarefas")
    if disciplinas is None or registros is None:
        return

    tarefas = [item for item in registros if _eh_tarefa(item)]
    notas = [item for item in registros if _eh_nota(item)]

    total_disciplinas = len(disciplinas)
    total_tarefas = len(tarefas)
    media_geral = 0

    if notas:
        df_notas = pd.DataFrame(notas)
        if "nota" in df_notas.columns:
            df_notas["nota"] = pd.to_numeric(df_notas["nota"], errors="coerce")
            media = df_notas["nota"].dropna().mean()
            media_geral = round(media, 1) if pd.notna(media) else 0

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
            candidatos_x = ["data", "created_at_nota", "nome_tarefa", "nome", "titulo", "id_nota", "disc_id"]
            nome_coluna = next((col for col in candidatos_x if col in df_plot.columns), None)
            if nome_coluna is None or df_plot.empty:
                st.info("Cadastre notas para visualizar gráficos.")
            else:
                fig = px.line(df_plot, x=nome_coluna, y="nota", color="nome_disciplina", markers=True)
                fig.update_layout(
                    paper_bgcolor="rgba(255,255,255,0)",
                    plot_bgcolor="rgba(248,235,244,0.92)",
                    font=dict(color="#1F2937"),
                    legend=dict(
                        bgcolor="rgba(248,235,244,0.92)",
                        bordercolor="rgba(31,41,55,0.12)",
                        borderwidth=1,
                        font=dict(color="#1F2937"),
                    ),
                    margin=dict(l=24, r=24, t=30, b=24),
                )
                fig.update_xaxes(
                    gridcolor="rgba(31,41,55,0.12)",
                    linecolor="rgba(31,41,55,0.25)",
                    tickfont=dict(color="#374151"),
                    title_font=dict(color="#374151"),
                )
                fig.update_yaxes(
                    gridcolor="rgba(31,41,55,0.16)",
                    linecolor="rgba(31,41,55,0.25)",
                    tickfont=dict(color="#374151"),
                    title_font=dict(color="#374151"),
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Cadastre notas para visualizar gráficos.")

    with col_lista:
        st.subheader("Próximas tarefas")
        if tarefas:
            for tarefa in sorted(tarefas, key=lambda t: str(t.get("data") or "9999-12-31"))[:5]:
                nome = escape(tarefa.get("nome_tarefa") or tarefa.get("nome") or "Tarefa")
                status = escape(tarefa.get("status") or "Pendente")
                prazo_raw = tarefa.get("data") or ""
                prazo = escape(str(prazo_raw)[:10] if prazo_raw else "Sem prazo")
                st.markdown(
                    f"""
                    <div class="automation-card">
                        <b>{nome}</b><br>
                        <span>{status} · {prazo}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhuma tarefa cadastrada.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Disciplinas")

    if disciplinas:
        cols = st.columns(2)
        for i, disc in enumerate(disciplinas):
            with cols[i % 2]:
                nome = escape(disc.get("nome_disciplina", "Disciplina"))
                st.markdown(
                    f"""
                    <div class="automation-card">
                        <b>{nome}</b><br>
                        <span>Continue evoluindo.</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Nenhuma disciplina cadastrada.")
