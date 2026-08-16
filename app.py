import streamlit as st
from pathlib import Path
from utils.theme import aplicar_tema
 
st.set_page_config(
    page_title="Portfólio | Quem sou eu",
    page_icon="👋",
    layout="wide",
)
 
aplicar_tema()
 
# ---------- Sidebar ----------
with st.sidebar:
    st.title("Seu Nome Aqui")
    st.caption("Estudante de Análise e Desenvolvimento de Sistemas")
    st.markdown("---")
    st.markdown("📧 seuemail@email.com")
    st.markdown("🔗 [LinkedIn](https://linkedin.com/in/seu-usuario)")
    st.markdown("💻 [GitHub](https://github.com/seu-usuario)")
 
# ---------- Conteúdo ----------
col_foto, col_texto = st.columns([1, 2], gap="large")
 
with col_foto:
    caminho_foto = Path("assets/foto_perfil.jpg")
    if caminho_foto.exists():
        st.image(str(caminho_foto), use_container_width=True)
    else:
        st.info("📷 Coloque sua foto em `assets/foto_perfil.jpg` para ela aparecer aqui.")
 
with col_texto:
    st.title("Olá, eu sou [Seu Nome] 👋")
    st.markdown(
        """
        Sou estudante de **[seu curso]** na **[sua instituição]**, apaixonado(a)
        por tecnologia e dados. Atualmente busco minha primeira oportunidade de
        **estágio em TI**, com interesse especial em [ex: dados, desenvolvimento
        de software, IA].
 
        > Escreva aqui 2-3 parágrafos curtos contando: quem você é, o que te
        > motiva na área de tecnologia, e o que você busca profissionalmente.
        > Evite textos muito longos — recrutadores leem rápido.
        """
    )
 
    st.markdown("### O que você vai encontrar aqui")
    st.markdown(
        """
        - 🎓 **Minhas Qualificações** — formação, projetos, hackathons e cursos.
        - 🛠️ **Skills** — competências técnicas, ferramentas e soft skills.
        - 📊 **Estudo de Mercado** — análise de dados sobre vagas de estágio em TI.
        """
    )
 
st.markdown("---")
st.caption("Dashboard desenvolvido para o Checkpoint de Data Science and Statistical Computing.")