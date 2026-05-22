import requests
import streamlit as st

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:HRRA97nd"


def get_headers():
    headers = {"Content-Type": "application/json"}

    if "auth_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"

    return headers


def api_get(endpoint):
    resposta = requests.get(f"{BASE_URL}/{endpoint}", headers=get_headers())
    return resposta.json() if resposta.status_code == 200 else []


def api_post(endpoint, dados):
    return requests.post(f"{BASE_URL}/{endpoint}", json=dados, headers=get_headers())


def api_delete(endpoint, item_id):
    return requests.delete(f"{BASE_URL}/{endpoint}/{item_id}", headers=get_headers())