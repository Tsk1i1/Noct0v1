import streamlit as st

st.set_page_config(page_title="Qualificações", page_icon="🎓", layout="wide")

st.title("🎓 Minhas Qualificações")
st.caption("Formação, cursos, certificações e experiências relevantes.")

st.markdown("### Formação Acadêmica")
st.markdown(
    """
    **Bacharelado em Engenharia de Software** — FIAP, Centro Universitário, São Paulo/SP
    Cursando o 4º semestre — conclusão prevista para dezembro de 2028.

    **Tecnólogo em Administração** — ETEC Prof.ª Luzia Maria Machado, Arujá/SP
    Concluído em dezembro de 2024.
    """
)

st.markdown("---")
st.markdown("### Projetos e Experiências")
st.caption("GS's, Hackathons, Nanocursos e Challenges — um expander por item.")

with st.expander("🎓 TCC — Como os avanços da IA vão impactar no meio empresarial (2024)"):
    st.markdown(
        """
        **Contexto:** Projeto de Conclusão de Curso do técnico em Administração,
        investigando os efeitos estratégicos e operacionais da adoção de
        Inteligência Artificial em empresas.

        **O que fiz:** pesquisa aprofundada sobre cenário atual e tendências
        do uso de IA; coleta e tratamento de dados para gráficos e
        relatórios; apresentação formal do projeto para uma banca avaliadora.

        **Resultado/Aprendizado:** aprendi a estruturar uma pesquisa aplicada
        do início ao fim e a comunicar resultados técnicos para um público
        avaliador — habilidades que uso até hoje.

        **Tecnologias:** `Pesquisa` `Análise de Dados` `Apresentação`
        """
    )

with st.expander("🌏 Global Solution: Conectaí (2025)"):
    st.markdown(
        """
        **Contexto:** Criação de uma aplicação web com foco em visualização de dados históricos e experiência interativa de usuário.

        **O que fiz:** Construção da interface com React, Vite e Tailwind CSS, integrada a painéis dinâmicos desenvolvidos em Python Dash e backend Node.js

        **Aplicação:** Criação de interfaces web dinamicas e funcionais.
        """
    )

with st.expander("💬 Engenharia de Prompt — Alura (2025)"):
    st.markdown(
        """
        **Instituição:** Alura

        **Conteúdo:** fundamentos de modelos de linguagem (LLMs), o conceito
        de *tokens* e *temperatura*, e técnicas de construção de prompts
        como Few-Shot e Chain-of-Thought.

        **Aplicação:** uso essas técnicas no dia a dia pra estudar mais
        rápido e prototipar ideias com ferramentas de IA.
        """
    )

with st.expander("🎨 Design Thinking — FIAP (2025)"):
    st.markdown(
        """
        **Instituição:** FIAP

        **Conteúdo:** metodologia de resolução de problemas centrada no
        usuário, com etapas de empatia, definição, ideação, prototipação e
        teste.

        **Aplicação:** usei a lógica de Design Thinking pra pensar a
        experiência de quem for avaliar este dashboard — o que essa pessoa
        precisa ver primeiro, e como organizar as informações de forma clara.
        """
    )

st.info(
    "💡 Duplique os blocos `st.expander` acima para cada projeto, hackathon, "
    "GS, nanocurso ou challenge que você quiser listar."
)
