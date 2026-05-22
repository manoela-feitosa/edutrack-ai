import streamlit as st

st.set_page_config(
    page_title="Disciplinas",
    page_icon="📚"
)

st.title("📚 Gestão de Disciplinas")

tab_lista, tab_novo = st.tabs([
    "📋 Listar",
    "➕ Nova Disciplina"
])

with tab_novo:
    st.subheader("Cadastrar Nova Matéria")

    with st.form("form_disciplina"):
        nome = st.text_input("Nome da Disciplina")
        professor = st.text_input("Nome do Professor")

        dia_semana = st.selectbox(
            "Dia da Aula",
            ["Seg", "Ter", "Qua", "Qui", "Sex"]
        )

        submitted = st.form_submit_button("Salvar")

        if submitted:
            st.success(
                f"Disciplina {nome} cadastrada!"
            )

with tab_lista:
    st.info(
        "A conexão com o Xano virá na Tarefa 13."
    )

    st.dataframe([
        {
            "Nome": "Python Basics",
            "Professor": "Oriel",
            "Dia": "Seg"
        },
        {
            "Nome": "No-Code Advanced",
            "Professor": "Giuliano",
            "Dia": "Qui"
        }
    ], use_container_width=True)