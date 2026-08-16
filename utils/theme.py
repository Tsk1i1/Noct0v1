"""
Controla o tema (claro/escuro) do dashboard.

Como o Streamlit multipage não permite alternar o `.streamlit/config.toml`
em tempo real, a técnica usada aqui é: manter a escolha do usuário numa
única chave de `st.session_state` ("tema") — a MESMA usada como `key` do
widget, sem passar `index` junto — e espelhar a escolha na URL via
`st.query_params`, que sobrevive até a um F5/reload completo.

Uso: chame `aplicar_tema()` como a primeira linha de cada página, logo
após `st.set_page_config(...)`. Para colorir gráficos Plotly de acordo
com o tema atual, use `cores_atuais()`.
"""

import streamlit as st

CORES_CLARO = {
    "fundo": "#ffffff",
    "fundo_secundario": "#f0f4f9",
    "texto": "#202124",
    "texto_secundario": "#5f6368",
    "primaria": "#1a73e8",
    "borda": "#e0e0e0",
    "grade": "#e0e0e0",
}

CORES_ESCURO = {
    "fundo": "#0e1117",
    "fundo_secundario": "#1c1f26",
    "texto": "#f0f2f6",
    "texto_secundario": "#b0b3b8",
    "primaria": "#4d9fff",
    "borda": "#333640",
    "grade": "#333640",
}


def tema_atual() -> str:
    """Retorna 'Claro' ou 'Escuro' — chama aplicar_tema() antes de usar."""
    return st.session_state.get("tema", "Claro")


def cores_atuais() -> dict:
    """Dicionário de cores do tema ativo, para usar em gráficos Plotly etc."""
    return CORES_ESCURO if tema_atual() == "Escuro" else CORES_CLARO


def aplicar_tema():
    """Renderiza o seletor de tema na sidebar e injeta o CSS correspondente."""

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

    # Sincroniza na URL: sobrevive a um F5 ou a um link direto pra outra página.
    st.query_params["tema"] = st.session_state.tema

    cores = cores_atuais()

    st.markdown(
        f"""
        <style>
        /* ---- Área principal do app ---- */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {cores['fundo']};
            color: {cores['texto']};
        }}
        [data-testid="stHeader"] {{
            background-color: transparent;
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background-color: {cores['fundo_secundario']};
        }}
        section[data-testid="stSidebar"] * {{
            color: {cores['texto']} !important;
        }}
        /* O Streamlit reduz a opacidade de rótulos de widget e legendas por
           padrão (efeito sutil pensado pro tema claro) — no fundo escuro
           isso fica ilegível, então forçamos opacidade total aqui. */
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label {{
            color: {cores['texto']} !important;
            opacity: 1 !important;
        }}

        /* ---- Textos genéricos ---- */
        h1, h2, h3, h4, h5, h6, p, span, label, li, div {{
            color: {cores['texto']};
        }}
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label {{
            color: {cores['texto']} !important;
            opacity: 1 !important;
        }}
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {cores['texto']} !important;
        }}
        .stMarkdown, .stCaption, [data-testid="stCaptionContainer"] {{
            color: {cores['texto_secundario']};
        }}

        /* ---- Expanders, dataframes ---- */
        div[data-testid="stExpander"] {{
            background-color: {cores['fundo_secundario']};
            border: 1px solid {cores['borda']};
            border-radius: 8px;
        }}
        [data-testid="stDataFrame"], [data-testid="stTable"] {{
            background-color: {cores['fundo_secundario']};
        }}

        /* ---- Botões ---- */
        .stButton>button, .stDownloadButton>button {{
            background-color: {cores['primaria']};
            color: #ffffff !important;
            border: none;
        }}

        /* ---- Caixas de multiselect/selectbox (a parte "fechada") ---- */
        [data-testid="stMultiSelect"] > div > div,
        [data-testid="stSelectbox"] > div > div,
        [data-baseweb="select"] > div {{
            background-color: {cores['fundo_secundario']} !important;
            color: {cores['texto']} !important;
            border-color: {cores['borda']} !important;
        }}
        [data-baseweb="tag"] {{
            background-color: {cores['primaria']} !important;
        }}

        /* ---- Dropdowns/menus: o Streamlit renderiza esses "popovers" fora
           do container principal (num portal anexado ao <body>), então
           precisam de seletores próprios — .stApp sozinho não alcança. ---- */
        div[data-baseweb="popover"] [role="listbox"],
        ul[data-testid="stSelectboxVirtualDropdown"],
        div[data-baseweb="menu"] {{
            background-color: {cores['fundo_secundario']} !important;
            color: {cores['texto']} !important;
        }}
        div[data-baseweb="popover"] li,
        div[data-baseweb="menu"] li,
        div[data-baseweb="menu"] span {{
            color: {cores['texto']} !important;
        }}
        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="menu"] li:hover {{
            background-color: {cores['borda']} !important;
        }}

        hr {{
            border-color: {cores['borda']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )