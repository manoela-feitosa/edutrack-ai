import pandas as pd
import streamlit as st

from api import api_get, api_post


def modulo_professores():
    st.header("Professores")

    with st.expander("Adicionar professor", expanded=True):
        nome = st.text_input("Nome do professor")
        email = st.text_input("E-mail de contato")

        if st.button("Cadastrar professor"):
            if not nome or not email:
                st.warning("Preencha o nome e o e-mail do professor.")
                return

            resposta = api_post("professores", {"nome": nome, "email": email})
            if resposta and resposta.status_code in [200, 201]:
                st.success("Professor cadastrado!")
                st.rerun()
            else:
                st.error("Erro ao cadastrar professor.")
                if resposta:
                    st.write(resposta.text)

    dados = api_get("professores")
    if dados:
        st.subheader("Professores cadastrados")
        df = pd.DataFrame(dados).rename(columns={"id": "Código", "nome": "Professor", "email": "E-mail"})
        st.dataframe(df[["Código", "Professor", "E-mail"]], use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum professor cadastrado ainda.")
