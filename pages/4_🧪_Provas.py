import streamlit as st

st.title("🧪 Provas")

tab_lista, tab_nova = st.tabs(["📋 Listar", "➕ Nova Prova"])

with tab_nova:
    st.subheader("Cadastrar Nova Prova")

    with st.form("form_prova"):
        disciplina = st.selectbox(
            "Disciplina",
            ["Python Basics", "No-Code Advanced", "Database Design", "Innovation Lab"]
        )

        tipo_prova = st.selectbox(
            "Tipo de Prova",
            ["AP1", "AP2", "Final", "Substitutiva"]
        )

        data = st.date_input("Data da Prova")
        peso = st.number_input("Peso da Prova", min_value=0.0, max_value=10.0, step=0.5)

        submitted = st.form_submit_button("Salvar")

        if submitted:
            st.success(f"Prova {tipo_prova} de {disciplina} cadastrada!")

with tab_lista:
    st.info("A conexão com o Xano virá nas próximas tarefas.")

    st.dataframe([
        {"Disciplina": "Python Basics", "Tipo": "AP1", "Data": "2026-05-20", "Peso": 10},
        {"Disciplina": "Database Design", "Tipo": "AP2", "Data": "2026-05-27", "Peso": 10},
    ], use_container_width=True)