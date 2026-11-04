import streamlit as st

from utils.ui import footer, page_header, setup_page, tags

setup_page("Competências", "Competências")
page_header(
    "Conhecimentos e prática",
    "As ferramentas por trás\ndos meus projetos.",
    "Tecnologias que uso e estudo, acompanhadas das atividades em que entram.",
)

col_tecnicas, col_trabalho = st.columns([1.65, 1], gap="large")

with col_tecnicas:
    st.header("Competências técnicas")
    competencias = [
        (
            "Python",
            "Análise de dados",
            "Tratamento de dados com pandas e construção deste dashboard "
            "com Streamlit e Plotly.",
        ),
        (
            "Java",
            "Programação",
            "Uma das linguagens que uso nos estudos de programação "
            "e lógica durante a graduação.",
        ),
        (
            "HTML, CSS e JavaScript",
            "Interfaces web",
            "Estudos e desenvolvimento de interfaces. No Conectaí, "
            "trabalhei com React, Vite e Tailwind CSS.",
        ),
        (
            "Arduino",
            "Eletrônica e programação",
            "Estudos e projetos com programação de placas e componentes eletrônicos.",
        ),
        (
            "SQL",
            "Banco de dados",
            "Conhecimento em desenvolvimento nos meus estudos de banco de dados.",
        ),
    ]
    for nome, area, aplicacao in competencias:
        with st.container(border=True):
            st.caption(area.upper())
            st.markdown(f"### {nome}")
            st.write(aplicacao)

with col_trabalho:
    st.header("Forma de trabalhar")
    st.write(
        "Gosto de desmontar problemas, entender suas partes e organizar "
        "uma solução. No TCC, pratiquei esse processo na pesquisa, "
        "no tratamento dos dados e na apresentação à banca."
    )
    tags([
        "Pensamento analítico",
        "Organização",
        "Foco em resultados",
        "Comunicação verbal",
        "Apresentação de projetos",
    ])

    st.divider()
    st.header("Ferramentas")
    tags(["Git / GitHub", "VS Code", "Arduino IDE", "Office", "Blender / Maya"])

    st.divider()
    st.header("Idiomas")
    st.write("Português · Nativo")
    st.write("Inglês · Intermediário")

st.divider()
st.page_link("pages/3_Estudo_de_Mercado.py", label="Ver Python aplicado no estudo de vagas")

footer()
