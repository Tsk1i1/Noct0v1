from pathlib import Path

import streamlit as st

from utils.ui import footer, setup_page, tags

setup_page("Apresentação", "Apresentação")

intro, portrait = st.columns([2.1, 1], gap="large", vertical_alignment="center")
with intro:
    st.html('''<header class="hero">
        <p class="eyebrow">Portfólio / Engenharia de software</p>
        <h1>Nicolas Mendes <br>dos Santos.</h1>
        <p class="lead">Gosto de desmontar problemas, entender suas partes e
        estruturar soluções. Estudo Engenharia de Software na FIAP e programo em Java e Python.</p>
        <p class="hero-role">Desenvolvimento de sistemas · Análise de dados</p>
    </header>''')
    st.link_button("Vamos conversar", "mailto:nico12571@hotmail.com", type="primary")
with portrait:
    with st.container(key="portrait"):
        photo = Path(__file__).resolve().parent / "assets/foto_perfil.jpg"
        if photo.exists():
            st.image(str(photo), width="stretch")
        st.caption("São Paulo, SP / Buscando minha primeira oportunidade de estágio")

st.divider()
st.html('<div class="section-label"><h2>Projeto em destaque</h2><span>01 / DADOS</span></div>')
with st.container(key="feature"):
    summary, workflow = st.columns([2, 1], gap="large")
    with summary:
        st.caption("ESTUDO DE MERCADO")
        st.subheader("Minha busca de estágio, vista pelos dados")
        st.write(
            "Registrei vagas de TI durante minha busca de estágio e analisei "
            "tecnologias exigidas, formatos de trabalho, benefícios e salários. "
            "O dashboard permite explorar esses dados e os motivos das minhas escolhas."
        )
        tags(["Python", "pandas", "Plotly", "Streamlit"])
        st.page_link("pages/3_Estudo_de_Mercado.py", label="Explorar o estudo de mercado →")
    with workflow:
        st.html('''<div class="data-workflow" aria-label="Etapas do projeto">
            <p>01<strong>Coleta</strong>Registro manual das vagas</p>
            <p>02<strong>Tratamento</strong>Limpeza e padronização</p>
            <p>03<strong>Análise</strong>Sete perguntas sobre a busca</p>
        </div>''')

st.html('<div class="section-label"><h2>Sobre meu percurso</h2><span>FORMAÇÃO &amp; PRÁTICA</span></div>')
about, focus = st.columns([1.5, 1], gap="large")
with about:
    st.write(
        "Sou técnico em Administração pela ETEC Prof.ª Luzia Maria Machado. "
        "No meu TCC, pesquisei como a inteligência artificial está mudando o meio empresarial, "
        "com coleta de dados, gráficos e apresentação dos resultados para uma banca."
    )
    st.write(
        "Hoje, na Engenharia de Software, me interesso por modelagem de informações, "
        "lógica e organização de sistemas. Busco um estágio para aplicar esse aprendizado em projetos reais."
    )
    st.page_link("pages/1_Qualificacoes.py", label="Ver formação e experiências →")
with focus:
    st.markdown("**O que estou desenvolvendo**")
    st.write("Programação em Java e Python, interfaces web e projetos com Arduino.")
    tags(["Desenvolvimento", "Dados", "Sistemas embarcados"])
    st.page_link("pages/2_Skills.py", label="Conhecer minhas competências →")

footer()
