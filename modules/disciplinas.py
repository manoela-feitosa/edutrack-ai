import pandas as pd
import streamlit as st

from api import api_get, api_post


def modulo_disciplinas():
    st.header("📚 Disciplinas")

    professores = api_get("professores")

    if not professores:
        st.warning("Cadastre um professor antes de criar disciplinas.")
        return

    opcoes_professores = {
        prof["nome"]: prof["id"]
        for prof in professores
    }

    with st.expander("➕ Nova Disciplina", expanded=True):
        nome = st.text_input("Nome da Disciplina")

        professor_escolhido = st.selectbox(
            "Professor Responsável",
            options=list(opcoes_professores.keys())
        )

        if st.button("Salvar Disciplina"):
            resposta = api_post(
                "disciplinas",
                {
                    "nome_disciplina": nome,
                    "prof_id": opcoes_professores[professor_escolhido]
                }
            )

            if resposta.status_code in [200, 201]:
                st.success("Disciplina cadastrada!")
                st.rerun()
            else:
                st.error("Erro ao cadastrar disciplina.")
                st.write(resposta.text)

    disciplinas = api_get("disciplinas")

    if disciplinas:
        st.subheader("Disciplinas cadastradas")

        df = pd.DataFrame(disciplinas)

        mapa_professores = {
            prof["id"]: prof["nome"]
            for prof in professores
        }

        df["Professor"] = df["prof_id"].map(mapa_professores)

        df = df.rename(columns={
            "id": "Código",
            "nome_disciplina": "Disciplina"
        })

        st.dataframe(
            df[["Código", "Disciplina", "Professor"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhuma disciplina cadastrada ainda.")