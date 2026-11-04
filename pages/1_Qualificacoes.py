import streamlit as st

from utils.ui import footer, page_header, setup_page, tags

setup_page("Qualificações", "Qualificações")
page_header(
    "Formação e experiência",
    "Um percurso entre\nadministração e tecnologia.",
    "Minha formação, os projetos em que trabalhei e os cursos que complementam meus estudos.",
)

st.header("Formação acadêmica")
col_atual, col_anterior = st.columns(2, gap="large")

with col_atual, st.container(border=True, key="formacao-atual"):
    st.caption("EM ANDAMENTO · CONCLUSÃO EM 2028")
    st.markdown("### Engenharia de Software")
    st.write("FIAP · São Paulo, SP")
    st.write("Bacharelado, 4º semestre. Conclusão prevista para dezembro de 2028.")

with col_anterior, st.container(border=True, key="formacao-anterior"):
    st.caption("CONCLUÍDO · 2024")
    st.markdown("### Administração")
    st.write("ETEC Prof.ª Luzia Maria Machado · Arujá, SP")
    st.write("Curso técnico concluído em dezembro de 2024.")

st.divider()
st.header("Projetos e experiências")
st.write("Pesquisa aplicada, desenvolvimento de interfaces e apresentação de resultados.")

with st.expander("Conectaí · Global Solution · 2025", expanded=True):
    st.write(
        "Aplicação web voltada à visualização de dados históricos, "
        "com uma experiência interativa para quem consulta os painéis."
    )
    st.write(
        "Trabalhei na construção da interface com React, Vite e Tailwind CSS, "
        "integrada a painéis em Python Dash e a um backend Node.js."
    )
    tags(["React", "Vite", "Tailwind CSS", "Python Dash", "Node.js"])

with st.expander("Inteligência artificial no meio empresarial · TCC · 2024"):
    st.write(
        "No TCC do técnico em Administração, investiguei como a adoção de "
        "inteligência artificial afeta a estratégia e a operação das empresas."
    )
    st.write(
        "Pesquisei o cenário e as tendências de uso de IA, coletei e tratei "
        "dados para gráficos e relatórios e apresentei o trabalho a uma banca. "
        "Foi minha primeira experiência de conduzir uma pesquisa aplicada "
        "do início à apresentação dos resultados."
    )
    tags(["Pesquisa", "Análise de dados", "Apresentação"])

st.divider()
st.header("Cursos complementares")

col_prompt, col_design = st.columns(2, gap="large")
with col_prompt, st.container(border=True, key="curso-prompt"):
    st.caption("ALURA · 2025")
    st.markdown("### Engenharia de Prompt")
    st.write(
        "Fundamentos de modelos de linguagem, tokens, temperatura e técnicas "
        "como Few-Shot e Chain-of-Thought. Uso esse conteúdo para estudar "
        "e prototipar ideias com ferramentas de IA."
    )

with col_design, st.container(border=True, key="curso-design"):
    st.caption("FIAP · 2025")
    st.markdown("### Design Thinking")
    st.write(
        "Empatia, definição do problema, ideação, prototipação e teste. "
        "Apliquei essa abordagem para organizar este portfólio e pensar "
        "no que quem visita precisa encontrar primeiro."
    )

footer()
