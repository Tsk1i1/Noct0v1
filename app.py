import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Portfólio | Quem sou eu",
    page_icon="👋",
    layout="wide",
)

# ---------- Sidebar ----------
with st.sidebar:
    st.title("Nicolas Mendes dos Santos")
    st.caption("Estudante de Engenharia de Software")
    st.markdown("---")
    st.markdown("📧 nico12571@hotmail.com")
    st.markdown("🔗 [LinkedIn](https://linkedin.com/in/tsuk1i1)")
    st.markdown("💻 [GitHub](https://github.com/Tsk1i1)")
    st.markdown("---")
    st.caption("🎨 Prefere tema escuro? Use o menu **⋮** (canto superior "
                "direito) → **Settings** → **Theme**.")

# ---------- Conteúdo ----------
col_foto, col_texto = st.columns([1, 2], gap="large")

with col_foto:
    caminho_foto = Path("assets/foto_perfil.jpg")
    if caminho_foto.exists():
        st.image(str(caminho_foto), use_container_width=True)
    else:
        st.info("📷 Coloque sua foto em `assets/foto_perfil.jpg` para ela aparecer aqui.")

with col_texto:
    st.title("Olá, eu sou Nicolas 👋")
    st.markdown(
        """
        Sou estudante de Engenharia de Software na FIAP e técnico em Administração pela ETEC Prof.ª Luzia Maria Machado. Meu perfil é naturalmente analítico — gosto de desmontar problemas complexos, entender suas partes e estruturar soluções que realmente façam sentido. Foi essa curiosidade que me levou, no TCC do técnico, a investigar como a Inteligência Artificial está transformando o meio empresarial e como os dados podem gerar decisões mais inteligentes.
        
        No dia a dia, programo em Java e Python, e me interesso cada vez mais pelo lado estratégico da tecnologia: como modelar informações, organizar processos e usar dados para encontrar respostas que não são óbvias à primeira vista. Gosto de pensar em arquitetura e lógica, não só em escrever código.
        
        Atualmente busco minha primeira oportunidade de estágio em Engenharia de Software, com interesse especial em tecnologia, inovação e áreas que envolvam análise de dados, resolução de problemas e estruturação de sistemas. Quero aplicar o que aprendo na faculdade em desafios reais e seguir evoluindo como alguém que constrói soluções com propósito.

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
