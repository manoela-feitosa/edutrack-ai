import streamlit as st

from services.api import exibir_erro_api


def sucesso_ou_erro(resposta, *, sucesso: str, erro: str) -> bool:
    if resposta is not None and resposta.status_code in {200, 201, 204}:
        st.success(sucesso)
        return True
    exibir_erro_api(resposta, erro)
    return False
