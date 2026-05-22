import streamlit as st

st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduTrack AI")

st.sidebar.header("Menu")

menu_option = st.sidebar.radio(
    "Navegar",
    ["Perfil", "Dashboard", "Disciplinas", "Provas", "Tarefas", "Notas", "Configurações"]
)

if menu_option == "Perfil":
    st.subheader("Perfil do Usuário")
    st.write("Informações do usuário")
elif menu_option == "Dashboard":
    st.write("Bem-vindo ao seu assistente acadêmico!")
    st.info("Conecte ao Xano para ver seus dados reais.")

    col1, col2 = st.columns(2)

    col1.metric("Disciplinas Ativas", "0")
    col2.metric("Tarefaz Pendentes", "0")

elif menu_option == "Disciplinas":
    st.subheader("Minhas Disciplinas")
    st.write("Aqui listaremos as matérias cadastradas no back-end.")
    st.button("Adicionar Disciplina")

elif menu_option == "Provas":
    st.subheader("Minhas Provas")
    st.write("Aqui listaremos as provas cadastradas no back-end.")
    st.button("Adicionar Prova")

elif menu_option == "Tarefas":
    st.subheader("Gerenciamento de Tarefas")
    st.write("Exemplo: Estudar Streamlit, Fazer Exercícios, etc.")
    st.button("Adicionar Tarefa")

elif menu_option == "Notas":
    st.subheader("Histórico de Notas")
    st.write("Visualize seu desempenho e acompanhe sua evolução acadêmica.")
    st.button("Adicionar Nota")

elif menu_option == "Configurações":
    st.subheader("Configurações")
    st.write("Ajustes e preferências da aplicação.")
    st.button("Salvar Configurações")
        
