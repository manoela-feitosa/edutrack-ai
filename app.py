import streamlit as st

st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

st.title("🎓 EduTrack AI")

st.sidebar.header("Menu")

pagina = st.sidebar.radio(
    "Navegar",
    ["Dashboard", "Perfil", "Disciplinas", "Provas", "Tarefas", "Notas", "Configurações"]
)

if pagina == "Dashboard":
    st.subheader("Dashboard")
    st.write("Bem-vinda ao EduTrack AI!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Disciplinas", "0")
    col2.metric("Tarefas", "0")
    col3.metric("Notas", "0")

elif pagina == "Perfil":
    exec(open("pages/1_👤_Perfil.py", encoding="utf-8").read())

elif pagina == "Disciplinas":
    exec(open("pages/2_📚_Disciplinas.py", encoding="utf-8").read())

elif pagina == "Tarefas":
    exec(open("pages/3_📝_Tarefas.py", encoding="utf-8").read())

elif pagina == "Provas":
    exec(open("pages/4_🧪_Provas.py", encoding="utf-8").read())

elif pagina == "Notas":
    exec(open("pages/5_📊_Notas.py", encoding="utf-8").read())

elif pagina == "Configurações":
    exec(open("pages/6_⚙️_Configurações.py", encoding="utf-8").read())