import streamlit as st

st.title("📊 Notas")

col1, col2, col3 = st.columns(3)

col1.metric("Média Geral", "7.5")
col2.metric("Maior Nota", "9.0")
col3.metric("Menor Nota", "5.8")

st.markdown("---")

tab_tabela, tab_lancar = st.tabs(["📋 Boletim", "➕ Lançar Nota"])

with tab_lancar:
    st.subheader("Lançar Nova Nota")

    with st.form("form_nota"):
        disciplina = st.selectbox(
            "Disciplina",
            ["Python Basics", "No-Code Advanced", "Database Design", "Innovation Lab"]
        )

        avaliacao = st.text_input("Avaliação", placeholder="Ex: AP2, Trabalho, Quiz")
        nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)

        submitted = st.form_submit_button("Salvar Nota")

        if submitted:
            st.success(f"Nota {nota} cadastrada para {disciplina}!")

with tab_tabela:
    st.dataframe([
        {"Disciplina": "Python Basics", "Avaliação": "AP1", "Nota": 8.5},
        {"Disciplina": "Database Design", "Avaliação": "Trabalho", "Nota": 9.0},
        {"Disciplina": "Innovation Lab", "Avaliação": "Projeto", "Nota": 7.5},
    ], use_container_width=True)

    st.bar_chart({
        "Notas": [8.5, 9.0, 7.5]
    })