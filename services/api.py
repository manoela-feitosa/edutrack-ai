import json
import time
from collections import deque

import requests
import streamlit as st

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:HRRA97nd"
TIMEOUT = 10
MAX_REQUESTS_PER_WINDOW = 8
RATE_WINDOW_SECONDS = 20
MAX_RETRIES = 3

_request_timestamps: deque[float] = deque()


def get_headers():
    headers = {"Content-Type": "application/json"}
    if "auth_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"
    return headers


def invalidar_cache():
    _cached_get.clear()


def _wait_for_rate_limit():
    now = time.monotonic()
    while _request_timestamps and now - _request_timestamps[0] >= RATE_WINDOW_SECONDS:
        _request_timestamps.popleft()

    if len(_request_timestamps) >= MAX_REQUESTS_PER_WINDOW:
        wait_seconds = RATE_WINDOW_SECONDS - (now - _request_timestamps[0]) + 0.25
        if wait_seconds > 0:
            time.sleep(wait_seconds)

    _request_timestamps.append(time.monotonic())


def _is_rate_limit(resposta: requests.Response) -> bool:
    if resposta.status_code == 429:
        return True
    try:
        payload = resposta.json()
    except ValueError:
        return False
    code = str(payload.get("code", "")).upper()
    message = str(payload.get("message", "")).lower()
    return "TOO_MANY_REQUESTS" in code or "too many" in message or "rate limit" in message


def _retry_delay(resposta: requests.Response | None, attempt: int) -> float:
    if resposta is not None:
        retry_after = resposta.headers.get("Retry-After")
        if retry_after and str(retry_after).isdigit():
            return float(retry_after)
    return min(RATE_WINDOW_SECONDS, 2 ** attempt + 1)


def _logout_por_sessao_expirada():
    st.error("Sua sessão expirou. Faça login novamente.")
    for chave in [
        "auth_token",
        "user_id",
        "user_name",
        "user_email",
        "user_curso",
        "user_semestre",
        "user_objetivo",
        "user_lembretes",
    ]:
        st.session_state.pop(chave, None)
    st.session_state.logged_in = False
    st.stop()


def mensagem_erro(resposta: requests.Response | None, padrao: str = "Não foi possível concluir a operação.") -> str:
    if resposta is None:
        return "Não foi possível conectar ao serviço. Tente novamente em instantes."
    if resposta.status_code == 429 or _is_rate_limit(resposta):
        return (
            "Limite de requisições do Xano atingido (10 a cada 20 segundos no plano gratuito). "
            "Aguarde cerca de 20 segundos e tente novamente."
        )
    if resposta.status_code in {401, 403}:
        return "Sua sessão expirou ou você não tem permissão para esta ação."
    try:
        payload = resposta.json()
        if isinstance(payload, dict) and payload.get("message"):
            return str(payload["message"])
    except ValueError:
        pass
    return padrao


def exibir_erro_api(resposta: requests.Response | None, padrao: str = "Não foi possível concluir a operação.") -> None:
    st.error(mensagem_erro(resposta, padrao))
    with st.expander("Detalhes do erro"):
        if resposta is None:
            st.code("Sem resposta do servidor.")
        else:
            st.code(resposta.text or f"HTTP {resposta.status_code}")


def _processar_resposta_get(resposta: requests.Response):
    if resposta.status_code == 200:
        return resposta.json()
    if resposta.status_code in {401, 403}:
        _logout_por_sessao_expirada()
    exibir_erro_api(resposta, "Não foi possível carregar as informações. Tente novamente.")
    return None


def api_request(method, endpoint, **kwargs):
    ultima_resposta = None

    for tentativa in range(MAX_RETRIES):
        _wait_for_rate_limit()
        try:
            resposta = requests.request(
                method,
                f"{BASE_URL}/{endpoint}",
                headers=get_headers(),
                timeout=TIMEOUT,
                **kwargs,
            )
        except requests.RequestException:
            st.error("Não foi possível conectar ao serviço. Tente novamente em instantes.")
            return None

        ultima_resposta = resposta
        if _is_rate_limit(resposta) and tentativa < MAX_RETRIES - 1:
            time.sleep(_retry_delay(resposta, tentativa))
            continue
        return resposta

    return ultima_resposta


@st.cache_data(ttl=45, show_spinner=False)
def _cached_get(endpoint: str, token_key: str) -> str:
    resposta = api_request("GET", endpoint)
    if resposta is None:
        raise RuntimeError("conexao")
    if resposta.status_code in {401, 403}:
        _logout_por_sessao_expirada()
    if resposta.status_code != 200:
        raise RuntimeError(resposta.text or f"HTTP {resposta.status_code}")
    return json.dumps(resposta.json())


def api_get(endpoint, *, use_cache: bool = True):
    token_key = st.session_state.get("auth_token", "")
    if use_cache and endpoint != "auth/me":
        try:
            return json.loads(_cached_get(endpoint, token_key))
        except RuntimeError as exc:
            if str(exc) == "conexao":
                return None
            st.error("Não foi possível carregar as informações. Tente novamente.")
            with st.expander("Detalhes do erro"):
                st.code(str(exc))
            return None

    resposta = api_request("GET", endpoint)
    if resposta is None:
        return None
    return _processar_resposta_get(resposta)


def api_post(endpoint, dados):
    resposta = api_request("POST", endpoint, json=dados)
    if resposta is not None and resposta.status_code in {200, 201}:
        invalidar_cache()
    return resposta


def api_patch(endpoint, item_id, dados):
    resposta = api_request("PATCH", f"{endpoint}/{item_id}", json=dados)
    if resposta is not None and resposta.status_code in {200, 201}:
        invalidar_cache()
    return resposta


def api_patch_endpoint(endpoint, dados):
    resposta = api_request("PATCH", endpoint, json=dados)
    if resposta is not None and resposta.status_code in {200, 201}:
        invalidar_cache()
    return resposta


def api_delete(endpoint, item_id):
    resposta = api_request("DELETE", f"{endpoint}/{item_id}")
    if resposta is not None and resposta.status_code in {200, 204}:
        invalidar_cache()
    return resposta


def api_delete_endpoint(endpoint):
    resposta = api_request("DELETE", endpoint)
    if resposta is not None and resposta.status_code in {200, 204}:
        invalidar_cache()
    return resposta
