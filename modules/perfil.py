import streamlit as st


def modulo_perfil():
    st.header("Perfil")

    nome_atual = st.session_state.get("user_name", "")
    email_atual = st.session_state.get("user_email", "")
    curso_atual = st.session_state.get("user_curso", "")
    semestre_atual = st.session_state.get("user_semestre", "")
    objetivo_atual = st.session_state.get("user_objetivo", "")
    lembretes_atual = st.session_state.get("user_lembretes", True)

    with st.container(border=True):
        st.subheader("Dados da conta")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Nome**")
            st.write(nome_atual or "Não informado")
            st.markdown("**Curso**")
            st.write(curso_atual or "Não informado")
            st.markdown("**Lembretes**")
            st.write("Ativados" if lembretes_atual else "Desativados")
        with col2:
            st.markdown("**E-mail**")
            st.write(email_atual or "Não informado")
            st.markdown("**Semestre**")
            st.write(semestre_atual or "Não informado")

    with st.container(border=True):
        st.subheader("Objetivo acadêmico")
        st.write(objetivo_atual or "Nenhum objetivo acadêmico cadastrado ainda.")

    with st.expander("Editar perfil", expanded=False):
        nome = st.text_input("Nome", value=nome_atual, placeholder="Digite seu nome")
        email = st.text_input("E-mail", value=email_atual, placeholder="Digite seu e-mail")
        curso = st.text_input("Curso", value=curso_atual, placeholder="Ex.: Sistemas de Informação")
        opcoes_semestre = [
            "Selecione o semestre",
            "1º semestre",
            "2º semestre",
            "3º semestre",
            "4º semestre",
            "5º semestre",
            "6º semestre",
            "7º semestre",
            "8º semestre",
        ]
        semestre = st.selectbox(
            "Semestre",
            opcoes_semestre,
            index=opcoes_semestre.index(semestre_atual) if semestre_atual in opcoes_semestre else 0,
        )
        objetivo = st.text_area(
            "Objetivo acadêmico",
            value=objetivo_atual,
            placeholder="Ex.: melhorar minhas notas e organizar melhor meus prazos",
        )
        lembretes = st.checkbox("Receber lembretes de tarefas", value=lembretes_atual)

        if st.button("Salvar perfil"):
            st.session_state.user_name = nome
            st.session_state.user_email = email
            st.session_state.user_curso = curso
            st.session_state.user_semestre = semestre if semestre != "Selecione o semestre" else ""
            st.session_state.user_objetivo = objetivo
            st.session_state.user_lembretes = lembretes
            st.success("Perfil salvo com sucesso!")
            st.rerun()
