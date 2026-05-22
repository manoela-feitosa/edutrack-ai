import streamlit as st


def modulo_perfil():
    st.header("👤 Perfil")

    nome = st.text_input(
        "Nome",
        value=st.session_state.get("user_name", "")
    )

    email = st.text_input(
        "E-mail",
        value=st.session_state.get("user_email", "")
    )

    curso = st.text_input("Curso", value="Sistemas de Informação")
    semestre = st.selectbox(
        "Semestre",
        ["1º semestre", "2º semestre", "3º semestre", "4º semestre",
         "5º semestre", "6º semestre", "7º semestre", "8º semestre"]
    )

    objetivo = st.text_area("Objetivo acadêmico")
    lembretes = st.checkbox("Receber lembretes de tarefas", value=True)

    if st.button("Salvar Perfil"):
        st.success("Perfil salvo com sucesso!")