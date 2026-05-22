import pandas as pd
import streamlit as st

from api import api_get, api_post


def modulo_notas():
    st.header("📊 Notas")

    disciplinas = api_get("disciplinas")

    if not disciplinas:
        st.warning("Cadastre uma disciplina primeiro.")
        return

    opcoes_disciplinas = {
        disc["nome_disciplina"]: disc["id"]
        for disc in disciplinas
    }

    with st.expander("➕ Lançar Nota", expanded=True):
        nome = st.text_input("Nome da Atividade/Avaliação")

        disciplina_escolhida = st.selectbox(
            "Disciplina",
            options=list(opcoes_disciplinas.keys())
        )

        nota = st.number_input(
            "Nota",
            min_value=0.0,
            max_value=10.0,
            value=0.0,
            step=0.1
        )

        data = st.date_input("Data da avaliação")

        if st.button("Salvar Nota"):
            resposta = api_post(
                "notas",
                {
                    "nome": nome,
                    "disc_id": opcoes_disciplinas[disciplina_escolhida],
                    "nota": nota,
                    "data": str(data)
                }
            )

            if resposta.status_code in [200, 201]:
                st.success("Nota cadastrada!")
                st.rerun()
            else:
                st.error("Erro ao cadastrar nota.")
                st.write(resposta.text)

    notas = api_get("notas")

    if notas:
        st.subheader("Notas cadastradas")

        df = pd.DataFrame(notas)

        mapa_disciplinas = {
            disc["id"]: disc["nome_disciplina"]
            for disc in disciplinas
        }

        df["Disciplina"] = df["disc_id"].map(mapa_disciplinas)

        df = df.rename(columns={
            "id": "Código",
            "nome": "Atividade",
            "nota": "Nota",
            "data": "Data"
        })

        st.dataframe(
            df[["Código", "Atividade", "Disciplina", "Nota", "Data"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhuma nota cadastrada ainda.")