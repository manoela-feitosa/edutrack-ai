import streamlit as st

st.title("⚙️ Configurações")

st.subheader("Preferências do Sistema")

with st.form("form_configuracoes"):
    tema = st.selectbox(
        "Tema visual",
        ["Claro", "Escuro", "Automático"]
    )

    notificacoes = st.checkbox("Receber lembretes de tarefas", value=True)

    frequencia = st.selectbox(
        "Frequência dos lembretes",
        ["Diariamente", "Semanalmente", "Somente no dia do prazo"]
    )

    salvar = st.form_submit_button("Salvar Configurações")

    if salvar:
        st.success("Configurações salvas com sucesso!")

st.markdown("---")

with st.expander("ℹ️ Sobre o EduTrack AI"):
    st.write("Projeto acadêmico desenvolvido na disciplina Innovation Lab.")
    st.write("Stack: Python, Streamlit, Xano, OpenSpec e GitHub.")