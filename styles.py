import streamlit as st


TEMAS = {
    "Oceano": {
        "bg1": "#E8F3F5",
        "bg2": "#D7E8EC",
        "bg3": "#EEF4F6",
        "text": "#1F2933",
        "muted": "#52616B",
        "primary": "#0F6B78",
        "primary2": "#2E8A99",
        "accent": "#D98E04",
        "card": "rgba(255,255,255,0.72)",
        "card_border": "rgba(15,107,120,0.18)",
        "shadow": "rgba(15,107,120,0.10)",
    },
    "Floresta": {
        "bg1": "#EEF4EE",
        "bg2": "#DCE9DF",
        "bg3": "#F6F2E8",
        "text": "#213027",
        "muted": "#5A6B60",
        "primary": "#2F6F4E",
        "primary2": "#4F8A63",
        "accent": "#B7791F",
        "card": "rgba(255,255,255,0.74)",
        "card_border": "rgba(47,111,78,0.18)",
        "shadow": "rgba(47,111,78,0.10)",
    },
    "Grafite": {
        "bg1": "#EEF1F4",
        "bg2": "#D9DEE5",
        "bg3": "#F5F6F8",
        "text": "#20262E",
        "muted": "#5D6673",
        "primary": "#344054",
        "primary2": "#596579",
        "accent": "#0E7490",
        "card": "rgba(255,255,255,0.76)",
        "card_border": "rgba(52,64,84,0.18)",
        "shadow": "rgba(52,64,84,0.10)",
    },
    "Rosé": {
        "bg1": "#FFF1F5",
        "bg2": "#F9DDE8",
        "bg3": "#F7EEF6",
        "text": "#3A2430",
        "muted": "#7A5B68",
        "primary": "#B8326A",
        "primary2": "#D85C88",
        "accent": "#8B5E83",
        "card": "rgba(255,255,255,0.78)",
        "card_border": "rgba(184,50,106,0.18)",
        "shadow": "rgba(184,50,106,0.11)",
    },
    "Lavanda": {
        "bg1": "#F5F0FF",
        "bg2": "#E6DDF7",
        "bg3": "#F8F3F8",
        "text": "#30273A",
        "muted": "#6E617A",
        "primary": "#7B61A8",
        "primary2": "#9B7ECD",
        "accent": "#C06C84",
        "card": "rgba(255,255,255,0.78)",
        "card_border": "rgba(123,97,168,0.20)",
        "shadow": "rgba(123,97,168,0.12)",
    },
    "Pêssego": {
        "bg1": "#FFF3EA",
        "bg2": "#F8DCCB",
        "bg3": "#FFF8F2",
        "text": "#3D2B25",
        "muted": "#7A6258",
        "primary": "#C4664A",
        "primary2": "#E08A68",
        "accent": "#9B5E78",
        "card": "rgba(255,255,255,0.80)",
        "card_border": "rgba(196,102,74,0.18)",
        "shadow": "rgba(196,102,74,0.11)",
    },
    "Claro": {
        "bg1": "#F7F7F2",
        "bg2": "#ECEDE7",
        "bg3": "#FFFFFF",
        "text": "#252A31",
        "muted": "#66717D",
        "primary": "#3A6EA5",
        "primary2": "#5B8DB8",
        "accent": "#C47F2C",
        "card": "rgba(255,255,255,0.82)",
        "card_border": "rgba(58,110,165,0.18)",
        "shadow": "rgba(58,110,165,0.09)",
    },
}


def carregar_css(nome_tema="Oceano"):
    tema = TEMAS.get(nome_tema, TEMAS["Oceano"])
    st.markdown(f"""
    <style>
    :root {{
        --bg1: {tema['bg1']};
        --bg2: {tema['bg2']};
        --bg3: {tema['bg3']};
        --text: {tema['text']};
        --muted: {tema['muted']};
        --primary: {tema['primary']};
        --primary2: {tema['primary2']};
        --accent: {tema['accent']};
        --card: {tema['card']};
        --card-border: {tema['card_border']};
        --shadow: {tema['shadow']};
    }}

    .stApp {{
        background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 52%, var(--bg3) 100%);
        color: var(--text);
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
        visibility: visible;
    }}

    #MainMenu,
    footer {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}

    [data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.54);
        border-right: 1px solid var(--card-border);
    }}

    .hero-login {{
        padding-top: 20px;
        padding-right: 10px;
    }}

    .logo-login {{
        font-size: 48px;
        font-weight: 760;
        color: var(--primary);
        margin-bottom: 48px;
    }}

    .logo-login span,
    .hero-login h1 span {{
        color: var(--accent);
    }}

    .hero-login h1 {{
        font-size: 52px !important;
        line-height: 1.08;
        color: var(--text);
        margin-bottom: 18px;
        font-weight: 740;
    }}

    .hero-login p {{
        font-size: 21px;
        color: var(--muted);
        line-height: 1.4;
        max-width: 650px;
        margin-bottom: 22px;
    }}

    .beneficio-card {{
        background: var(--card);
        border-radius: 24px;
        min-height: 176px;
        padding: 26px 24px;
        text-align: center;
        border: 1px solid var(--card-border);
        box-shadow: 0 14px 34px var(--shadow);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}

    .beneficio-icone {{
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: color-mix(in srgb, var(--primary) 14%, white);
        color: var(--primary);
        font-size: 22px;
        font-weight: 760;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 18px;
    }}

    .beneficio-card b {{
        display: block;
        margin-bottom: 14px;
        font-size: 24px;
        color: var(--primary);
    }}

    .beneficio-card small {{
        font-size: 18px;
        color: var(--text);
        line-height: 1.5;
    }}

    div[data-testid="stTabs"] {{
        background: var(--card);
        border: 1px solid var(--card-border);
        border-radius: 22px;
        padding: 42px;
        margin-top: 130px;
        box-shadow: 0 22px 70px var(--shadow);
    }}

    button[data-baseweb="tab"] {{
        color: var(--text) !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: var(--primary) !important;
    }}

    div[data-testid="stForm"] {{
        border: none;
        padding: 0;
    }}

    label {{
        font-weight: 700 !important;
        color: var(--text) !important;
    }}

    input,
    textarea {{
        border-radius: 12px !important;
        border: 1px solid rgba(31,41,51,0.18) !important;
        background: white !important;
        padding: 15px !important;
        font-size: 16px !important;
        color: var(--text) !important;
    }}

    input:focus,
    textarea:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }}

    div[data-testid="stFormSubmitButton"] {{
        width: 100%;
    }}

    div[data-testid="stFormSubmitButton"] button,
    .stButton > button {{
        width: 100% !important;
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary2) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 24px var(--shadow);
    }}

    div[data-testid="stFormSubmitButton"] button {{
        min-height: 64px !important;
        border-radius: 18px !important;
        font-size: 20px !important;
    }}

    div[data-testid="stFormSubmitButton"] button:hover,
    .stButton > button:hover {{
        transform: translateY(-1px);
        opacity: 0.96;
        color: white !important;
        border: none !important;
    }}

    div[data-testid="metric-container"],
    div[data-testid="stExpander"],
    .automation-card {{
        background: var(--card);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        box-shadow: 0 8px 24px var(--shadow);
    }}

    div[data-testid="metric-container"],
    div[data-testid="stExpander"] {{
        padding: 18px;
    }}

    .stDataFrame {{
        background: var(--card);
        border-radius: 16px;
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {{
        border-radius: 12px !important;
        border: 1px solid rgba(31,41,51,0.18) !important;
        background: white !important;
        padding: 15px !important;
        font-size: 16px !important;
    }}

    div[data-testid="stSelectbox"] input {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        width: 0 !important;
        min-width: 0 !important;
    }}

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {{
        background: rgba(255,255,255,0.78) !important;
        border-radius: 12px !important;
        border-color: var(--card-border) !important;
    }}

    h1, h2, h3, h4 {{
        color: var(--text);
        letter-spacing: 0;
    }}

    .automation-card {{
        padding: 16px 18px;
        margin-bottom: 12px;
        color: var(--text);
        overflow-wrap: anywhere;
    }}

    .automation-card b {{
        color: var(--primary);
        font-size: 17px;
    }}

    .automation-card span,
    .automation-card small {{
        color: var(--muted);
        line-height: 1.5;
    }}

    .calendar-preview {{
        margin-top: 12px;
    }}

    @media (max-width: 900px) {{
        .block-container {{
            padding-top: 2rem;
        }}
        .logo-login {{
            font-size: 40px;
            margin-bottom: 35px;
        }}
        .hero-login h1 {{
            font-size: 42px !important;
            line-height: 1.08;
            margin-bottom: 18px;
        }}
        .hero-login p {{
            font-size: 18px;
        }}
        div[data-testid="stTabs"] {{
            padding: 32px;
            margin-top: 40px;
            border-radius: 22px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


