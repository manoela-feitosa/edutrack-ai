import streamlit as st


def carregar_css():
    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #F6F1FF, #EDE9FE);
        color: #1E1B4B;
    }

    section[data-testid="stSidebar"] {
        background-color: #DDD6FE;
        border-right: 1px solid #C4B5FD;
    }

    .stButton > button {
        background-color: #7C3AED;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #6D28D9;
        color: white;
    }

    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #E9D5FF;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    h1, h2, h3 {
        color: #4C1D95;
    }

    </style>
    """, unsafe_allow_html=True)