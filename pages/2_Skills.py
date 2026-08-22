import streamlit as st

st.set_page_config(page_title="Skills", page_icon="🛠️", layout="wide")

st.title("🛠️ Skills")
st.caption("Competências técnicas, ferramentas, idiomas e soft skills.")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 💻 Hard Skills")
    hard_skills = {
        "Python": 0.65,
        "Java": 0.65,
        "HTML / CSS / Javascript": 0.6,
        "Arduino": 0.5,
        "SQL": 0.45,
        
    }
    for skill, nivel in hard_skills.items():
        st.markdown(f"**{skill}**")
        st.progress(nivel)

    st.markdown("### 🌐 Idiomas")
    idiomas = {
        "Português": "Nativo",
        "Inglês": "Intermediário",
    }
    for idioma, nivel in idiomas.items():
        st.markdown(f"- **{idioma}:** {nivel}")

with col2:
    st.markdown("### 🤝 Soft Skills")
    soft_skills = [
        "Pensamento analítico",
        "Organização",
        "Foco em resultados",
        "Comunicação verbal",
        "Apresentação de projetos",
    ]
    tags_html = " ".join(
        f'<span style="background-color:#e8f0fe;color:#1a73e8;padding:6px 12px;'
        f'border-radius:16px;margin:4px;display:inline-block;font-size:14px;">{s}</span>'
        for s in soft_skills
    )
    st.markdown(tags_html, unsafe_allow_html=True)

    st.markdown("### 🧰 Ferramentas")
    ferramentas = ["Git/GitHub", "VS Code", "Arduino IDE", "Office", "Blender/Maya",]
    st.markdown("\n".join(f"- {f}" for f in ferramentas))

