"""Transparent charts inherit the active Streamlit theme, including live changes."""


def cores_atuais() -> dict:
    return {
        "fundo": "rgba(0,0,0,0)",
        "texto": None,  # Streamlit supplies the theme font color to Plotly.
        "grade": "rgba(128,128,128,0.18)",
    }
