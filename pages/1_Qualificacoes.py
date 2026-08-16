import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.theme import aplicar_tema  # noqa: E402

st.set_page_config(page_title="Qualificações", page_icon="🎓", layout="wide")

aplicar_tema()

st.title("🎓 Minhas Qualificações")
st.caption("Formação, cursos, certificações e experiências relevantes.")

st.markdown("### Formação Acadêmica")
st.markdown(
    """
    **[Nome do curso]** — [Instituição]
    [Mês/Ano de início] – [Mês/Ano previsto de conclusão]
    """
)

st.markdown("---")
st.markdown("### Projetos e Experiências")
st.caption("GS's, Hackathons, Nanocursos e Challenges — um expander por item.")

# Exemplo de item — duplique este bloco para cada GS/Hackathon/Nanocurso/Challenge
with st.expander("🏆 [Nome do Hackathon/GS/Challenge] — [Mês/Ano]"):
    st.markdown(
        """
        **Contexto:** breve descrição do desafio proposto.

        **O que fiz:** sua contribuição específica no projeto.

        **Resultado/Aprendizado:** o que você entregou ou aprendeu com a experiência.

        **Tecnologias:** `Python` `SQL` `...`
        """
    )

with st.expander("📘 [Nome do Nanocurso/Certificação] — [Mês/Ano]"):
    st.markdown(
        """
        **Instituição/Plataforma:** [ex: Alura, Coursera, FIAP]

        **Conteúdo:** o que foi abordado no curso.

        **Aplicação:** onde você já usou ou pretende usar esse conhecimento.
        """
    )

st.info(
    "💡 Duplique os blocos `st.expander` acima para cada projeto, hackathon, "
    "GS, nanocurso ou challenge que você quiser listar."
)
