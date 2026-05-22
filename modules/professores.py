import pandas as pd
import streamlit as st

from api import api_get, api_post


def modulo_professores():
    st.header("👨‍🏫 Professores")

    with st.expander("➕ Adicionar Professor", expanded=True):
        nome = st.text_input("Nome do Professor")
        email = st.text_input("E-mail de Contato")

        if st.button("Cadastrar Professor"):
            resposta = api_post(
                "professores",
                {
                    "nome": nome,
                    "email": email
                }
            )

            if resposta.status_code in [200, 201]:
                st.success("Professor cadastrado!")
                st.rerun()
            else:
                st.error("Erro ao cadastrar professor.")
                st.write(resposta.text)

    dados = api_get("professores")

    if dados:
        st.subheader("Professores cadastrados")

        df = pd.DataFrame(dados)

        df = df.rename(columns={
            "id": "Código",
            "nome": "Professor",
            "email": "E-mail"
        })

        st.dataframe(
            df[["Código", "Professor", "E-mail"]],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Nenhum professor cadastrado ainda.")