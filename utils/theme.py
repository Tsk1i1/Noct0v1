"""
Controla o tema (claro/escuro) do dashboard.

Como o Streamlit multipage não permite alternar o `.streamlit/config.toml`
em tempo real, a técnica usada aqui é: manter a escolha do usuário numa
única chave de `st.session_state` ("tema") — a MESMA usada como `key` do
widget, sem passar `index` junto (passar os dois ao mesmo tempo é a causa
mais comum de o valor "voltar ao padrão" ao trocar de página) — e também
espelhar a escolha na URL via `st.query_params`, que sobrevive mesmo a uma
navegação/reload completo do navegador.

Uso: chame `aplicar_tema()` como a primeira linha de cada página, logo
após `st.set_page_config(...)`.
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

    # Semeia o estado inicial ANTES de criar o widget (só na primeira vez
    # que essa página roda na sessão). Depois disso, quem manda no valor
    # é o próprio widget via key="tema" — nunca escrevemos em
    # st.session_state["tema"] manualmente de novo, pra evitar o conflito
    # "default value + Session State API" que causava o bug entre páginas.
    if "tema" not in st.session_state:
        tema_na_url = st.query_params.get("tema")
        st.session_state.tema = tema_na_url if tema_na_url in ("Claro", "Escuro") else "Claro"

    with st.sidebar:
        st.radio(
            "🎨 Tema",
            options=["Claro", "Escuro"],
            horizontal=True,
            key="tema",
        )

    # Mantém a URL sincronizada, garantindo que o tema sobreviva mesmo a um
    # F5 / link direto para outra página (não só a navegação interna).
    st.query_params["tema"] = st.session_state.tema

    cores = CORES_ESCURO if st.session_state.tema == "Escuro" else CORES_CLARO

    st.markdown(
        f"""
        <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {cores['fundo']};
            color: {cores['texto']};
        }}

        [data-testid="stHeader"] {{
            background-color: transparent;
        }}

        section[data-testid="stSidebar"] {{
            background-color: {cores['fundo_secundario']};
        }}

        section[data-testid="stSidebar"] * {{
            color: {cores['texto']} !important;
        }}

        h1, h2, h3, h4, h5, h6, p, span, label, li, div {{
            color: {cores['texto']};
        }}

        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {cores['texto']} !important;
        }}

        .stMarkdown, .stCaption, [data-testid="stCaptionContainer"] {{
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

        [data-testid="stDataFrame"], [data-testid="stTable"] {{
            background-color: {cores['fundo_secundario']};
        }}

        hr {{
            border-color: {cores['borda']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )