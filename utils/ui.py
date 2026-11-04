"""Shared presentation layer; native controls retain theme and focus states."""

from html import escape
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
PAGES = (
    ("app.py", "Apresentação", "01"),
    ("pages/1_Qualificacoes.py", "Qualificações", "02"),
    ("pages/2_Skills.py", "Competências", "03"),
    ("pages/3_Estudo_de_Mercado.py", "Estudo de mercado", "04"),
)


def setup_page(title: str, section: str) -> None:
    st.set_page_config(page_title=f"{title} | Nicolas Mendes", page_icon=":material/terminal:",
                       layout="wide", initial_sidebar_state="auto")
    st.html((ROOT / "assets/styles.css").read_text(encoding="utf-8"))
    with st.sidebar:
        st.html('<div class="identity"><span class="monogram" aria-hidden="true">nm.</span>'
                '<p class="identity-name">Nicolas Mendes</p>'
                '<p class="identity-detail">Engenharia de Software<br>FIAP · São Paulo</p></div>')
        st.caption("PORTFÓLIO / NAVEGAÇÃO")
        for path, label, number in PAGES:
            st.page_link(path, label=f"{number}  {label}", use_container_width=True)
        st.divider()
        st.html('<p class="availability"><span aria-hidden="true"></span>Em busca de estágio</p>')
        st.markdown("[LinkedIn](https://linkedin.com/in/tsuk1i1) · [GitHub](https://github.com/Tsk1i1)")
        st.markdown("[Entrar em contato](mailto:nico12571@hotmail.com)")
        st.caption("Escolha o tema claro ou escuro no menu do canto superior.")


def page_header(eyebrow: str, title: str, description: str) -> None:
    title_html = escape(title).replace("\n", "<br>")
    st.html(f'<header class="page-heading"><p class="eyebrow">{escape(eyebrow)}</p>'
            f'<h1>{title_html}</h1><p class="lead">{escape(description)}</p></header>')


def tags(items: list[str]) -> None:
    labels = "".join(f'<li>{escape(item)}</li>' for item in items)
    st.html(f'<ul class="tags" aria-label="Tecnologias e áreas">{labels}</ul>')


def footer() -> None:
    st.divider()
    st.html('<footer class="page-footer"><span>Nicolas Mendes dos Santos</span>'
            '<span>Engenharia de software &amp; análise de dados</span></footer>')
