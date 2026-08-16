"""
Controla o tema (claro/escuro) do dashboard.
"""

import streamlit as st

CORES_CLARO = {
    "fundo": "#ffffff",
    "fundo_secundario": "#f0f4f9",
    "texto": "#202124",
    "texto_secundario": "#5f6368",
    "primaria": "#1a73e8",
    "borda": "#e0e0e0",
}

CORES_ESCURO = {
    "fundo": "#0e1117",
    "fundo_secundario": "#1c1f26",
    "texto": "#f0f2f6",
    "texto_secundario": "#b0b3b8",
    "primaria": "#4d9fff",
    "borda": "#333640",
}


def aplicar_tema():
    """Renderiza o seletor de tema na sidebar e injeta o CSS correspondente."""
    if "tema" not in st.session_state:
        st.session_state.tema = "Claro"

    with st.sidebar:
        st.session_state.tema = st.radio(
            "🎨 Tema",
            options=["Claro", "Escuro"],
            index=0 if st.session_state.tema == "Claro" else 1,
            horizontal=True,
            key="seletor_tema",
        )

    cores = CORES_ESCURO if st.session_state.tema == "Escuro" else CORES_CLARO

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {cores['fundo']};
            color: {cores['texto']};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {cores['fundo_secundario']};
        }}

        section[data-testid="stSidebar"] * {{
            color: {cores['texto']} !important;
        }}

        h1, h2, h3, h4, h5, h6, p, span, label, li {{
            color: {cores['texto']} !important;
        }}

        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {cores['texto']} !important;
        }}

        .stMarkdown, .stCaption {{
            color: {cores['texto_secundario']};
        }}

        div[data-testid="stExpander"] {{
            background-color: {cores['fundo_secundario']};
            border: 1px solid {cores['borda']};
            border-radius: 8px;
        }}

        .stButton>button, .stDownloadButton>button {{
            background-color: {cores['primaria']};
            color: #ffffff !important;
            border: none;
        }}

        hr {{
            border-color: {cores['borda']};
        }}

        [data-testid="stDataFrame"] {{
            background-color: {cores['fundo_secundario']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )