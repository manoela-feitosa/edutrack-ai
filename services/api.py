import requests
import streamlit as st

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:HRRA97nd"
TIMEOUT = 10


def get_headers():
    # Monta os headers da requisicao e inclui o token quando o usuario esta logado.
    headers = {"Content-Type": "application/json"}
    if "auth_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"
    return headers


def api_request(method, endpoint, **kwargs):
    # Funcao central usada por GET, POST, PATCH e DELETE para chamar o Xano.
    try:
        return requests.request(
            method,
            f"{BASE_URL}/{endpoint}",
            headers=get_headers(),
            timeout=TIMEOUT,
            **kwargs,
        )
    except requests.RequestException:
        st.error("Não foi possível conectar ao serviço. Tente novamente em instantes.")
        return None


def api_get(endpoint):
    # Busca dados no Xano e trata sessao expirada de forma amigavel.
    resposta = api_request("GET", endpoint)
    if resposta is None:
        return None
    if resposta.status_code == 200:
        return resposta.json()
    if resposta.status_code in [401, 403]:
        st.error("Sua sessão expirou. Faça login novamente.")
        for chave in ["auth_token", "user_id", "user_name", "user_email"]:
            st.session_state.pop(chave, None)
        st.session_state.logged_in = False
        st.stop()
    st.error("Não foi possível carregar as informações. Tente novamente.")
    return None


def api_post(endpoint, dados):
    # Cria registros no Xano.
    return api_request("POST", endpoint, json=dados)


def api_patch(endpoint, item_id, dados):
    # Atualiza um registro especifico pelo id.
    return api_request("PATCH", f"{endpoint}/{item_id}", json=dados)


def api_patch_endpoint(endpoint, dados):
    # Atualiza endpoints sem id na URL, como dados do usuario logado.
    return api_request("PATCH", endpoint, json=dados)


def api_delete(endpoint, item_id):
    # Exclui um registro especifico pelo id.
    return api_request("DELETE", f"{endpoint}/{item_id}")


def api_delete_endpoint(endpoint):
    # Exclui usando endpoint direto, como excluir a propria conta.
    return api_request("DELETE", endpoint)
