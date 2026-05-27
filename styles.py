import streamlit as st


def carregar_css():
    st.markdown("""
    <style>

    .stApp {

        background:
        linear-gradient(
            135deg,
            #FDF2F8 0%,
            #F5F3FF 50%,
            #EFF6FF 100%
        );

        color: #312E81;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {

        background:
        linear-gradient(
            180deg,
            #F9A8D4 0%,
            #C084FC 100%
        );

        border-right: 1px solid #F5D0FE;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 28px;
        font-weight: 700;
    }

    .hero-login {

        padding-top: 60px;
        padding-right: 40px;
    }

    .logo-login {

        font-size: 52px;
        font-weight: 800;
        color: #4C1D95;
        margin-bottom: 30px;
    }

    .logo-login span {
        color: #EC4899;
    }

    .hero-login h1 {

        font-size: 72px !important;
        line-height: 1.1;
        color: #312E81;
        margin-bottom: 20px;
    }

    .hero-login h1 span {
        color: #C084FC;
    }

    .hero-login p {

        font-size: 22px;
        color: #6D28D9;
        line-height: 1.7;
        max-width: 600px;
    }

    .beneficios {

        display: flex;
        gap: 20px;
        margin-top: 50px;
    }

    .beneficios div {

        background: rgba(255,255,255,0.55);

        backdrop-filter: blur(12px);

        padding: 24px;

        border-radius: 24px;

        text-align: center;

        min-width: 160px;

        box-shadow:
        0 8px 24px rgba(168,85,247,0.08);
    }

    .login-box {

        background: rgba(255,255,255,0.55);

        backdrop-filter: blur(18px);

        border: 1px solid rgba(255,255,255,0.4);

        border-radius: 36px;

        padding: 45px;

        margin-top: 40px;

        box-shadow:
        0 8px 32px rgba(192,132,252,0.15);
    }

    .login-icon {

        width: 80px;
        height: 80px;

        border-radius: 50%;

        background:
        linear-gradient(
            135deg,
            #F9A8D4,
            #C084FC
        );

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 34px;

        margin-bottom: 20px;
    }

    .login-box h2 {

        font-size: 42px;
        color: #5B21B6;
        margin-bottom: 8px;
    }

    .login-box p {

        color: #7C3AED;
        margin-bottom: 25px;
    }

    .stButton > button {

        width: 100%;

        background:
        linear-gradient(
            90deg,
            #EC4899,
            #A855F7
        );

        color: white;

        border: none;

        border-radius: 18px;

        padding: 0.95rem;

        font-size: 18px;

        font-weight: 700;

        box-shadow:
        0 8px 20px rgba(236,72,153,0.25);
    }

    .stButton > button:hover {
        opacity: 0.95;
        color: white;
    }

    input, textarea {

        border-radius: 18px !important;

        border: 1px solid #F5D0FE !important;

        background: rgba(255,255,255,0.75) !important;

        padding: 14px !important;
    }

    div[data-testid="metric-container"] {

        background: rgba(255,255,255,0.65);

        backdrop-filter: blur(14px);

        border: 1px solid rgba(255,255,255,0.5);

        border-radius: 24px;

        padding: 20px;

        box-shadow:
        0 8px 24px rgba(168,85,247,0.08);
    }

    div[data-testid="stExpander"] {

        background: rgba(255,255,255,0.55);

        backdrop-filter: blur(12px);

        border-radius: 24px;

        border: 1px solid rgba(255,255,255,0.4);

        box-shadow:
        0 8px 24px rgba(168,85,247,0.08);
    }

    .stDataFrame {

        background: rgba(255,255,255,0.55);

        border-radius: 24px;
    }

    </style>
    """, unsafe_allow_html=True)