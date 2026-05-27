import pandas as pd
import plotly.express as px
import streamlit as st

from api import api_get


def modulo_dashboard():

    st.markdown("""
    <h1 style='font-size:48px;'>
        ✨ Olá, Manu!
    </h1>

    <p style='font-size:20px; color:#7C3AED;'>
        Que bom te ver de novo 💖
    </p>
    """, unsafe_allow_html=True)

    professores = api_get("professores")
    disciplinas = api_get("disciplinas")
    tarefas = api_get("tarefas")
    notas = api_get("notas")

    total_disciplinas = len(disciplinas)
    total_tarefas = len(tarefas)

    media_geral = 0

    if notas:
        df_notas = pd.DataFrame(notas)

        if "nota" in df_notas.columns:
            media_geral = round(df_notas["nota"].mean(), 1)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Disciplinas",
            total_disciplinas
        )

    with col2:
        st.metric(
            "📝 Tarefas",
            total_tarefas
        )

    with col3:
        st.metric(
            "⭐ Média Geral",
            media_geral
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_grafico, col_lista = st.columns([2, 1])

    with col_grafico:

        st.subheader("📈 Desempenho Acadêmico")

        if notas and disciplinas:

            df_notas = pd.DataFrame(notas)
            df_disciplinas = pd.DataFrame(disciplinas)

            df_plot = df_notas.merge(
                df_disciplinas,
                left_on="disc_id",
                right_on="id",
                suffixes=("_nota", "_disciplina")
            )

            fig = px.line(
                df_plot,
                x="nome",
                y="nota",
                color="nome_disciplina",
                markers=True
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#4C1D95"),
                margin=dict(l=20, r=20, t=30, b=20)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("Cadastre notas para visualizar gráficos.")

    with col_lista:

        st.subheader("🔥 Próximas Tarefas")

        if tarefas:

            for tarefa in tarefas[:5]:

                nome = tarefa.get("nome_tarefa", "Tarefa")
                status = tarefa.get("status", "Pendente")

                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.55);
                    padding:16px;
                    border-radius:18px;
                    margin-bottom:12px;
                    border:1px solid #F5D0FE;
                ">
                    <b>{nome}</b><br>
                    <span style='color:#7C3AED'>
                        {status}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("Nenhuma tarefa cadastrada.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("💜 Disciplinas")

    if disciplinas:
        cols = st.columns(2)

        for i, disc in enumerate(disciplinas):
            with cols[i % 2]:
                nome = disc.get("nome_disciplina", "Disciplina")

                card = f"""
                <div style="
                    background: rgba(255,255,255,0.6);
                    padding: 22px;
                    border-radius: 24px;
                    margin-bottom: 18px;
                    border: 1px solid #F5D0FE;
                    box-shadow: 0 8px 24px rgba(168,85,247,0.08);
                ">
                    <h4 style="color:#7C3AED; margin-bottom:8px;">
                        📚 {nome}
                    </h4>
                    <p style="color:#6D28D9; margin:0;">
                        Continue evoluindo ✨
                    </p>
                </div>
                """

                st.markdown(card, unsafe_allow_html=True)
    else:
        st.info("Nenhuma disciplina cadastrada.")