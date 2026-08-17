"""
Detecta o tema nativo do Streamlit (claro/escuro), escolhido pelo próprio
usuário no menu ⋮ → Settings → Theme, para colorir os gráficos Plotly de
forma compatível.

Esse módulo NÃO injeta mais CSS customizado. A versão anterior tentava
"forçar" um tema escuro via CSS por cima de um app configurado como claro,
e isso deixava alguns componentes nativos (dropdowns, menus) sem tema
correto, porque eles pegam a cor de dentro do próprio Streamlit/BaseWeb,
não do CSS externo. A solução robusta é deixar o Streamlit cuidar do tema
de verdade — por isso `.streamlit/config.toml` não trava mais
`backgroundColor`/`textColor`, o que libera o alternador de tema nativo
(que reconfigura TODOS os componentes corretamente, sem exceção).
"""

import streamlit as st

CORES_CLARO = {
    "fundo": "#ffffff",
    "texto": "#202124",
    "grade": "#e0e0e0",
}

CORES_ESCURO = {
    "fundo": "#0e1117",
    "texto": "#f0f2f6",
    "grade": "#333640",
}


def tema_atual() -> str:
    """
    Retorna 'Claro' ou 'Escuro' conforme o tema nativo ativo no navegador
    do usuário (definido em ⋮ → Settings → Theme). Requer Streamlit
    razoavelmente recente (st.context.theme); em versões mais antigas onde
    isso não existir, assume 'Claro' como padrão seguro.
    """
    try:
        return "Escuro" if st.context.theme.type == "dark" else "Claro"
    except Exception:
        return "Claro"


def cores_atuais() -> dict:
    """Dicionário de cores do tema ativo, para usar em gráficos Plotly."""
    return CORES_ESCURO if tema_atual() == "Escuro" else CORES_CLARO
