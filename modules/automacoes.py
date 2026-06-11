from datetime import date, timedelta
from html import escape

import pandas as pd
import streamlit as st

from api import api_get


def _valor(item, *nomes, padrao=""):
    for nome in nomes:
        if nome in item and item.get(nome) not in [None, ""]:
            return item.get(nome)
    return padrao


def _disciplinas_por_id(disciplinas):
    return {disc.get("id"): disc.get("nome_disciplina", "Disciplina") for disc in disciplinas}


def _eh_tarefa(item):
    return item.get("tipo", "tarefa") != "nota"


def _tarefas_pendentes(tarefas):
    pendentes = []
    for tarefa in tarefas:
        status = str(_valor(tarefa, "status", padrao="Pendente")).lower()
        if "concl" not in status:
            pendentes.append(tarefa)
    return pendentes


def _df_desempenho(disciplinas, registros):
    if not disciplinas:
        return pd.DataFrame(columns=["disc_id", "Disciplina", "Media", "Qtd notas"])

    mapa = _disciplinas_por_id(disciplinas)
    notas = [item for item in registros if item.get("tipo") == "nota"]
    if not notas:
        return pd.DataFrame(
            [{"disc_id": disc_id, "Disciplina": nome, "Media": 0.0, "Qtd notas": 0} for disc_id, nome in mapa.items()]
        )

    df = pd.DataFrame(notas)
    if "disc_id" not in df.columns or "nota" not in df.columns:
        return pd.DataFrame(columns=["disc_id", "Disciplina", "Media", "Qtd notas"])

    df["nota"] = pd.to_numeric(df["nota"], errors="coerce").fillna(0)
    desempenho = df.groupby("disc_id").agg(Media=("nota", "mean"), **{"Qtd notas": ("nota", "count")}).reset_index()
    desempenho["Disciplina"] = desempenho["disc_id"].map(mapa).fillna("Disciplina")
    desempenho["Media"] = desempenho["Media"].round(1)
    return desempenho[["disc_id", "Disciplina", "Media", "Qtd notas"]].sort_values("Media")


def _recomendacoes(desempenho):
    mensagens = []
    for item in desempenho.to_dict("records"):
        if item["Media"] == 0:
            continue
        if item["Media"] < 6:
            mensagens.append(f"{item['Disciplina']} está com média {item['Media']:.1f}. Priorize uma revisão nesta semana.")
        elif item["Media"] < 7:
            mensagens.append(f"{item['Disciplina']} precisa de atenção antes da próxima avaliação.")
    return mensagens


def _opcoes_atividades(desempenho, tarefas):
    atividades = []
    if not desempenho.empty:
        for item in desempenho.to_dict("records"):
            disciplina = item.get("Disciplina")
            if disciplina:
                atividades.append(f"Estudar {disciplina}")

    for tarefa in _tarefas_pendentes(tarefas):
        nome = _valor(tarefa, "nome_tarefa", "nome", "titulo", padrao="")
        if nome:
            atividades.append(f"Avançar em {nome}")

    return list(dict.fromkeys(atividades))


def _plano_estudos(desempenho, tarefas):
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    opcoes = _opcoes_atividades(desempenho, tarefas)
    if not opcoes:
        return pd.DataFrame(columns=["Dia", "Atividade", "Duração", "Prioridade"])

    plano = []
    for i, dia in enumerate(dias):
        atividade = opcoes[i % len(opcoes)]
        plano.append(
            {
                "Dia": dia,
                "Atividade": atividade,
                "Duração": "2h" if atividade.startswith("Avançar em ") else "1h",
                "Prioridade": "Alta" if i < min(3, len(opcoes)) else "Média",
            }
        )
    return pd.DataFrame(plano)


def _progresso_tarefas(tarefas):
    total = len(tarefas)
    if total == 0:
        return 0
    concluidas = total - len(_tarefas_pendentes(tarefas))
    return round((concluidas / total) * 100)


def _boletim(disciplinas, tarefas, registros):
    desempenho = _df_desempenho(disciplinas, registros)
    pendentes = _tarefas_pendentes(tarefas)
    validas = desempenho[desempenho["Media"] > 0] if not desempenho.empty else desempenho
    melhor = validas.sort_values("Media", ascending=False).iloc[0]["Disciplina"] if not validas.empty else "Sem notas"
    dificuldade = validas.sort_values("Media").iloc[0]["Disciplina"] if not validas.empty else "Sem notas"
    media = round(float(validas["Media"].mean()), 1) if not validas.empty else 0
    return {
        "Média atual": media,
        "Tarefas concluídas": len(tarefas) - len(pendentes),
        "Tarefas pendentes": len(pendentes),
        "Melhor disciplina": melhor,
        "Disciplina com mais dificuldade": dificuldade,
    }


def _calendar_payload(nome_tarefa, disciplina, data_entrega):
    data_iso = data_entrega.isoformat() if hasattr(data_entrega, "isoformat") else str(data_entrega)
    return {
        "summary": nome_tarefa,
        "description": f"Entrega de {disciplina} criada pelo EduTrack AI.",
        "start": {"date": data_iso},
        "end": {"date": data_iso},
        "status": "google_calendar_ready",
    }


def _render_boletim(boletim):
    c1, c2, c3 = st.columns(3)
    c1.metric("Média atual", boletim["Média atual"])
    c2.metric("Concluídas", boletim["Tarefas concluídas"])
    c3.metric("Pendentes", boletim["Tarefas pendentes"])
    melhor = escape(str(boletim["Melhor disciplina"]))
    dificuldade = escape(str(boletim["Disciplina com mais dificuldade"]))
    st.markdown(
        f"""
        <div class="automation-card"><b>Melhor disciplina</b><br><span>{melhor}</span></div>
        <div class="automation-card"><b>Mais dificuldade</b><br><span>{dificuldade}</span></div>
        """,
        unsafe_allow_html=True,
    )


def modulo_automacoes():
    st.header("Central de Rotina")
    st.caption("Acompanhe alertas, metas, boletim semanal, calendário e organização da rotina acadêmica.")

    disciplinas = api_get("disciplinas")
    registros = api_get("tarefas")
    if disciplinas is None or registros is None:
        return
    tarefas = [item for item in registros if _eh_tarefa(item)]
    desempenho = _df_desempenho(disciplinas, registros)
    pendentes = _tarefas_pendentes(tarefas)
    recomendacoes = _recomendacoes(desempenho)
    progresso = _progresso_tarefas(tarefas)

    col1, col2, col3 = st.columns(3)
    col1.metric("Progresso", f"{progresso}%")
    col2.metric("Pendentes", len(pendentes))
    col3.metric("Alertas", len(recomendacoes))

    st.subheader("Resumo da rotina")
    if tarefas:
        st.info(f"Você concluiu {progresso}% das tarefas cadastradas.")
    if pendentes:
        st.warning(f"Existem {len(pendentes)} tarefas pendentes para priorizar.")
    else:
        st.success("Todas as tarefas cadastradas estão concluídas.")

    for mensagem in recomendacoes:
        st.warning(mensagem)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Boletim semanal")
        _render_boletim(_boletim(disciplinas, tarefas, registros))

    with col_b:
        st.subheader("Lembretes de tarefas")
        if pendentes:
            for tarefa in pendentes[:6]:
                nome = escape(_valor(tarefa, "nome_tarefa", "nome", "titulo", padrao="Tarefa"))
                status = escape(_valor(tarefa, "status", padrao="Pendente"))
                st.markdown(f"<div class='automation-card'><b>{nome}</b><br><span>{status}</span></div>", unsafe_allow_html=True)
        else:
            st.success("Nenhuma tarefa pendente.")

    st.subheader("Google Calendar")
    with st.expander("Preparar evento de calendário", expanded=True):
        nomes_disciplinas = {disc.get("nome_disciplina", "Disciplina"): disc.get("id") for disc in disciplinas}
        nome_tarefa = st.text_input("Nome do evento", "Trabalho de Banco de Dados")
        disciplina = st.selectbox("Disciplina", list(nomes_disciplinas.keys()) or ["Disciplina"])
        data_entrega = st.date_input("Data de entrega", value=date.today() + timedelta(days=7), format="DD/MM/YYYY")
        payload = _calendar_payload(nome_tarefa, disciplina, data_entrega)
        st.markdown(
            f"""
            <div class="automation-card calendar-preview">
                <b>{escape(payload['summary'])}</b><br>
                <span>{escape(payload['description'])}</span><br>
                <small>Data: {data_entrega.strftime('%d/%m/%Y')}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Cronograma automático")
    plano = _plano_estudos(desempenho, tarefas)
    if plano.empty:
        st.info("Cadastre pelo menos uma disciplina ou tarefa para gerar o cronograma automático.")
    else:
        st.data_editor(
            plano,
            use_container_width=True,
            hide_index=True,
            disabled=["Dia"],
            column_config={
                "Atividade": st.column_config.SelectboxColumn("Atividade", options=_opcoes_atividades(desempenho, tarefas), required=True),
                "Duração": st.column_config.SelectboxColumn("Duração", options=["30min", "1h", "1h30", "2h", "3h", "4h"], required=True),
                "Prioridade": st.column_config.SelectboxColumn("Prioridade", options=["Baixa", "Média", "Alta"], required=True),
            },
            key="editor_cronograma_rotina",
        )
