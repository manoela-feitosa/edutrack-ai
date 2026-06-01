import requests
import streamlit as st

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:HRRA97nd"
TIMEOUT = 10


def get_headers():
    headers = {"Content-Type": "application/json"}
    if "auth_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"
    return headers


def api_request(method, endpoint, **kwargs):
    try:
        return requests.request(
            method,
            f"{BASE_URL}/{endpoint}",
            headers=get_headers(),
            timeout=TIMEOUT,
            **kwargs,
        )
    except requests.RequestException as exc:
        st.error(f"Erro ao comunicar com a API: {exc}")
        return None


def api_get(endpoint):
    resposta = api_request("GET", endpoint)
    if resposta is None:
        return []
    if resposta.status_code == 200:
        return resposta.json()
    st.error(f"Erro ao carregar dados de {endpoint}. Status: {resposta.status_code}")
    return []


def api_post(endpoint, dados):
    return api_request("POST", endpoint, json=dados)


def api_patch(endpoint, item_id, dados):
    return api_request("PATCH", f"{endpoint}/{item_id}", json=dados)


def api_delete(endpoint, item_id):
    return api_request("DELETE", f"{endpoint}/{item_id}")
