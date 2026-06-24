import streamlit as st


TEMAS = {
    "Céu Estrelado": {
        "bg1": "#0F172A",
        "bg2": "#312E81",
        "bg3": "#1E1B4B",
        "bg4": "#3B1D5F",
        "text": "#F8FAFC",
        "muted": "#D7DDFB",
        "primary": "#1E3A8A",
        "primary2": "#4C1D95",
        "accent": "#38BDF8",
        "card": "rgba(255,255,255,0.13)",
        "card_border": "rgba(255,255,255,0.24)",
        "shadow": "rgba(15,23,42,0.34)",
        "input_bg": "rgba(255,255,255,0.94)",
        "input_text": "#241B33",
        "input_border": "rgba(255,255,255,0.32)",
        "surface": "rgba(255,255,255,0.13)",
        "surface_solid": "#1E1B4B",
        "star_overlay": True,
    },
    "Obsidiana": {
        "bg1": "#050509",
        "bg2": "#111827",
        "bg3": "#24162F",
        "bg4": "#1E1B4B",
        "text": "#F9FAFB",
        "muted": "#C7D2FE",
        "primary": "#4F46E5",
        "primary2": "#1D4ED8",
        "accent": "#818CF8",
        "card": "rgba(255,255,255,0.12)",
        "card_border": "rgba(255,255,255,0.20)",
        "shadow": "rgba(0,0,0,0.42)",
        "input_bg": "rgba(255,255,255,0.94)",
        "input_text": "#111827",
        "input_border": "rgba(255,255,255,0.30)",
        "surface": "rgba(255,255,255,0.12)",
        "surface_solid": "#24162F",
        "star_overlay": True,
    },
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
    "Algodão Doce": {
        "bg1": "#F8D7E8",
        "bg2": "#DCC7F0",
        "bg3": "#D8E5F7",
        "text": "#3A2430",
        "muted": "#7A5B68",
        "primary": "#EC4899",
        "primary2": "#A855F7",
        "accent": "#A855F7",
        "card": "rgba(255,255,255,0.82)",
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
    bg4 = tema.get("bg4", tema["bg3"])
    input_bg = tema.get("input_bg", "white")
    input_text = tema.get("input_text", tema["text"])
    input_border = tema.get("input_border", "rgba(31,41,51,0.18)")
    surface = tema.get("surface", "rgba(255,255,255,0.84)")
    surface_solid = tema.get("surface_solid", "#FFFFFF")
    app_background = (
        "radial-gradient(circle at 16% 18%, rgba(255,255,255,0.34) 0 1px, transparent 1.8px),"
        "radial-gradient(circle at 76% 16%, rgba(255,255,255,0.24) 0 1px, transparent 1.8px),"
        "radial-gradient(circle at 48% 68%, rgba(255,255,255,0.18) 0 1px, transparent 1.8px),"
        "linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 42%, var(--bg3) 72%, var(--bg4) 100%)"
        if tema.get("star_overlay")
        else "linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 52%, var(--bg3) 100%)"
    )
    st.markdown(f"""
    <style>
    :root {{
        color-scheme: light;
        --bg1: {tema['bg1']};
        --bg2: {tema['bg2']};
        --bg3: {tema['bg3']};
        --bg4: {bg4};
        --text: {tema['text']};
        --muted: {tema['muted']};
        --primary: {tema['primary']};
        --primary2: {tema['primary2']};
        --accent: {tema['accent']};
        --card: {tema['card']};
        --card-border: {tema['card_border']};
        --shadow: {tema['shadow']};
        --input-bg: {input_bg};
        --input-text: {input_text};
        --input-border: {input_border};
        --surface: {surface};
        --surface-solid: {surface_solid};
    }}

    .stApp {{
        background: {app_background};
        background-attachment: fixed;
        color: var(--text);
        color-scheme: light;
    }}

    html,
    body,
    [data-testid="stAppViewContainer"] {{
        color-scheme: light;
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
        background: rgba(255,255,255,0.62);
        border-right: 1px solid var(--card-border);
    }}

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] * {{
        color: var(--text) !important;
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
        width: 86px;
        height: 86px;
        border-radius: 50%;
        background: color-mix(in srgb, var(--primary) 14%, white);
        color: var(--primary);
        font-size: 45px;
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
        background: var(--surface);
        border: 1px solid var(--card-border);
        border-radius: 22px;
        padding: 42px;
        margin-top: 130px;
        box-shadow: 0 22px 70px var(--shadow);
    }}

    button[data-baseweb="tab"] {{
        color: var(--muted) !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: var(--primary) !important;
    }}

    .forgot-password-link {{
        display: block;
        width: fit-content;
        margin: 14px 0 0 0;
        color: var(--muted) !important;
        font-weight: 700;
        text-decoration: none !important;
    }}

    .forgot-password-inline {{
        margin: 26px 0 0 auto;
        text-align: right;
        white-space: nowrap;
    }}

    .forgot-password-link:hover {{
        color: var(--primary) !important;
        text-decoration: underline !important;
    }}

    div[data-testid="stForm"] {{
        border: none;
        padding: 0;
        background: transparent !important;
    }}

    label {{
        font-weight: 700 !important;
        color: var(--text) !important;
    }}

    input,
    textarea {{
        border-radius: 12px !important;
        border: 1px solid var(--input-border) !important;
        background: var(--input-bg) !important;
        padding: 15px !important;
        font-size: 16px !important;
        color: var(--input-text) !important;
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
        background: var(--surface);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        box-shadow: 0 8px 24px var(--shadow);
    }}

    div[data-testid="metric-container"],
    div[data-testid="stExpander"] {{
        padding: 18px;
    }}

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] details * {{
        color: var(--text) !important;
    }}

    .stDataFrame {{
        background: var(--surface);
        border-radius: 16px;
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {{
        border-radius: 12px !important;
        border: 1px solid var(--input-border) !important;
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
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
        background: var(--input-bg) !important;
        border-radius: 12px !important;
        border: 1px solid var(--input-border) !important;
        color: var(--input-text) !important;
    }}

    div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] div {{
        color: var(--input-text) !important;
    }}

    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] div[role="listbox"] {{
        background: var(--surface-solid) !important;
    }}

    div[data-testid="stDataFrame"],
    div[data-testid="stDataFrame"] *,
    div[data-testid="stTable"],
    div[data-testid="stTable"] * {{
        color-scheme: light;
    }}

    div[data-testid="stDataFrame"] div,
    div[data-testid="stDataFrame"] span,
    div[data-testid="stDataFrame"] p {{
        color: var(--text) !important;
    }}

    div[data-testid="stExpander"] {{
        color-scheme: light;
    }}

    div[data-testid="stExpander"] > details {{
        background: var(--surface) !important;
        border-radius: 16px !important;
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

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {{
        visibility: hidden !important;
        height: 0 !important;
        position: fixed !important;
    }}

    .app-ambient-bg {{
        position: fixed;
        z-index: 0;
        pointer-events: none;
        right: -220px;
        top: 72px;
        width: min(48vw, 760px);
        opacity: .18;
        filter: saturate(1.08);
    }}

    [data-testid="stSidebar"] {{
        background: rgba(255,255,255,.86) !important;
        border-right: 1px solid rgba(168,85,247,.16);
        box-shadow: 18px 0 55px rgba(110,69,183,.08);
    }}

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: .85rem;
    }}

    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 10px 0 14px;
    }}

    .sidebar-brand-title {{
        font-size: 1.12rem;
        font-weight: 820;
        color: #1F2937;
        line-height: 1.1;
    }}

    .sidebar-brand-title span {{
        color: #A855F7;
    }}

    .sidebar-brand-subtitle {{
        font-size: .72rem !important;
    }}

    .sidebar-user-card {{
        display: flex;
        align-items: center;
        gap: 10px;
        background: #F8F5FF;
        border: 1px solid rgba(168,85,247,.14);
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 8px;
        box-shadow: 0 8px 22px rgba(110,69,183,.07);
    }}

    .sidebar-user-card strong {{
        display: block;
        color: #1F2937 !important;
        font-size: .92rem;
        line-height: 1.1;
    }}

    .sidebar-user-card small {{
        display: block;
        max-width: 170px;
        color: #6B7280 !important;
        font-size: .72rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }}

    .sidebar-divider {{
        height: 1px;
        background: rgba(168,85,247,.16);
        margin: 12px 0 4px;
    }}

    .theme-picker-label {{
        margin: 8px 0 -4px;
        color: #6B7280;
        font-size: .78rem;
        font-weight: 800;
    }}

    .brand-mark,
    .avatar {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        color: white !important;
        background: linear-gradient(135deg, #EC4899, #A855F7);
        box-shadow: 0 8px 20px rgba(168,85,247,.28);
    }}

    .brand-mark {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        font-size: 20px;
    }}

    .avatar {{
        width: 38px;
        height: 38px;
        border-radius: 999px;
        font-weight: 800;
        font-size: .86rem;
    }}

    div[role="radiogroup"] label {{
        border-radius: 12px;
        padding: 8px 10px;
        transition: background .16s ease, transform .16s ease;
    }}

    div[role="radiogroup"] label:hover {{
        background: #F8F5FF;
    }}

    div[role="radiogroup"] label:has(input:checked) {{
        background: linear-gradient(135deg, rgba(236,72,153,.12), rgba(168,85,247,.12));
        color: #A855F7 !important;
        font-weight: 800 !important;
    }}

    .dashboard-hero {{
        position: relative;
        overflow: hidden;
        min-height: 230px;
        margin-bottom: 18px;
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,.78);
        background:
            radial-gradient(circle at 82% 30%, rgba(168,85,247,.34), transparent 30%),
            linear-gradient(135deg, rgba(255,255,255,.94), rgba(248,245,255,.78));
        padding: 28px 32px;
        box-shadow: 0 20px 60px rgba(110,69,183,.12);
        backdrop-filter: blur(16px);
    }}

    .dashboard-hero h2 {{
        font-size: 2rem;
        line-height: 1.16;
        margin: 10px 0;
        max-width: 560px;
        color: #171044;
    }}

    .dashboard-hero p {{
        max-width: 540px;
        color: #5B4B86;
        line-height: 1.55;
        margin: 0;
        font-size: 1rem;
    }}

    .dashboard-hero .hero-books {{
        position: absolute;
        right: -24px;
        bottom: -78px;
        width: min(45%, 430px);
        filter: drop-shadow(0 26px 38px rgba(78,42,170,.22));
    }}

    .hero-kpis {{
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 22px;
        max-width: 600px;
    }}

    .mini-stat {{
        min-width: 124px;
        padding: 10px 13px;
        border-radius: 12px;
        background: rgba(255,255,255,.82);
        border: 1px solid rgba(168,85,247,.14);
    }}

    .mini-stat b {{
        display: block;
        color: #171044;
        font-size: 1.05rem;
    }}

    .mini-stat span {{
        color: #6B7280;
        font-size: .72rem;
        font-weight: 700;
    }}

    .pill {{
        display: inline-flex;
        align-items: center;
        width: fit-content;
        border-radius: 999px;
        padding: 6px 10px;
        background: #F3E8FF;
        color: #A855F7;
        font-size: .78rem;
        font-weight: 800;
    }}

    .soft-card,
    .card {{
        background: rgba(255,255,255,.78);
        border: 1px solid rgba(255,255,255,.80);
        border-radius: 22px;
        box-shadow: 0 20px 60px rgba(110,69,183,.12);
        backdrop-filter: blur(16px);
    }}

    div[data-testid="metric-container"] {{
        background: rgba(255,255,255,.82) !important;
        border: 1px solid rgba(168,85,247,.14) !important;
        border-radius: 18px !important;
        box-shadow: 0 12px 34px rgba(110,69,183,.10) !important;
    }}

    .automation-card {{
        background: rgba(255,255,255,.82) !important;
        border: 1px solid rgba(168,85,247,.14) !important;
        border-radius: 18px !important;
        box-shadow: 0 12px 34px rgba(110,69,183,.10) !important;
    }}

    @media (max-width: 900px) {{
        .app-ambient-bg {{
            width: 860px;
            right: -560px;
            top: 80px;
            opacity: .12;
        }}
        .dashboard-hero {{
            padding: 22px;
            min-height: 420px;
        }}
        .dashboard-hero .hero-books {{
            width: 92%;
            right: -60px;
            bottom: -76px;
        }}
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


