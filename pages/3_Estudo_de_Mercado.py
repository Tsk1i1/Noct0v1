import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Permite importar utils/ quando a página roda dentro de pages/
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data_loader import carregar_dados, tecnologias_mais_frequentes  # noqa: E402
from utils.theme import aplicar_tema  # noqa: E402

st.set_page_config(page_title="Estudo de Mercado", page_icon="📊", layout="wide")

aplicar_tema()

# Os gráficos plotly têm fundo próprio (branco por padrão) e não seguem o
# CSS injetado — por isso trocamos o template deles conforme o tema escolhido.
TEMPLATE_GRAFICO = "plotly_dark" if st.session_state.get("tema") == "Escuro" else "plotly_white"

st.title("📊 Estudo de Mercado — Vagas de Estágio em TI")
st.caption(
    "Base de dados própria, construída manualmente a partir de vagas de estágio "
    "de TI encontradas durante minha busca por oportunidades."
)

df = carregar_dados()

# ---------------- Filtros ----------------
with st.sidebar:
    st.header("Filtros")
    nichos = st.multiselect(
        "Nicho de mercado", options=sorted(df["Nicho de Mercado"].dropna().unique()),
        default=None,
    )
    tipos_trabalho = st.multiselect(
        "Tipo de trabalho", options=sorted(df["Tipo de Trabalho"].dropna().unique()),
        default=None,
    )

df_filtrado = df.copy()
if nichos:
    df_filtrado = df_filtrado[df_filtrado["Nicho de Mercado"].isin(nichos)]
if tipos_trabalho:
    df_filtrado = df_filtrado[df_filtrado["Tipo de Trabalho"].isin(tipos_trabalho)]

# ---------------- Métricas gerais ----------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Vagas analisadas", len(df_filtrado))
c2.metric("Empresas distintas", df_filtrado["Nome da Empresa"].nunique())
c3.metric(
    "Vagas de interesse",
    int(df_filtrado["Interessante"].sum()) if "Interessante" in df_filtrado else 0,
)
c4.metric(
    "% com salário divulgado",
    f'{df_filtrado["Salário"].notna().mean() * 100:.0f}%' if "Salário" in df_filtrado else "N/A",
)

st.markdown("---")

# ---------------- Pergunta 1: quais tecnologias mais aparecem? ----------------
st.subheader("1. Quais tecnologias mais aparecem nas vagas?")
col_a, col_b = st.columns([1, 3])
with col_a:
    apenas_interesse = st.checkbox("Somente vagas do meu interesse", value=False)
with col_b:
    freq_tec = tecnologias_mais_frequentes(df_filtrado, apenas_interessantes=apenas_interesse)
    if not freq_tec.empty:
        fig_tec = px.bar(
            freq_tec.sort_values(ascending=True),
            orientation="h",
            labels={"value": "Nº de vagas", "index": "Tecnologia"},
            title=None,
            template=TEMPLATE_GRAFICO,
        )
        fig_tec.update_layout(showlegend=False, yaxis_title="", xaxis_title="Nº de vagas")
        st.plotly_chart(fig_tec, use_container_width=True)
    else:
        st.info("Nenhuma tecnologia registrada para o filtro selecionado.")

st.markdown(
    """
    **Insight (edite com sua leitura real dos dados):** descreva aqui qual
    tecnologia mais aparece e o que isso sugere sobre o que priorizar nos
    estudos (ex: "Python e SQL aparecem juntos em X% das vagas, reforçando
    que são a base mais exigida para estágios de TI").
    """
)

st.markdown("---")

# ---------------- Pergunta 2: presencial x híbrido x remoto ----------------
st.subheader("2. Como se distribuem os tipos de trabalho?")
col_c, col_d = st.columns(2)

with col_c:
    dist_tipo = df_filtrado["Tipo de Trabalho"].value_counts()
    fig_tipo = px.pie(
        values=dist_tipo.values, names=dist_tipo.index, hole=0.4,
        template=TEMPLATE_GRAFICO,
    )
    st.plotly_chart(fig_tipo, use_container_width=True)

with col_d:
    if "Interessante" in df_filtrado.columns:
        cross = (
            df_filtrado.groupby(["Tipo de Trabalho", "Interessante"])
            .size()
            .reset_index(name="Vagas")
        )
        cross["Interessante"] = cross["Interessante"].map({True: "Sim", False: "Não"})
        fig_cross = px.bar(
            cross, x="Tipo de Trabalho", y="Vagas", color="Interessante",
            barmode="group", template=TEMPLATE_GRAFICO,
        )
        st.plotly_chart(fig_cross, use_container_width=True)

st.markdown(
    """
    **Insight (edite):** relacione o tipo de trabalho com o quanto a vaga te
    interessa. Ex: "a maioria das vagas recusadas por incompatibilidade de
    horário era presencial, o que sugere priorizar buscas por híbrido/remoto".
    """
)

st.markdown("---")

# ---------------- Pergunta 3: por que as vagas não interessam? ----------------
st.subheader("3. Quando uma vaga não me interessa, por quê?")
if "Justificativa" in df_filtrado.columns:
    justificativas = df_filtrado["Justificativa"].dropna()
    if not justificativas.empty:
        fig_just = px.bar(justificativas.value_counts(), template=TEMPLATE_GRAFICO)
        fig_just.update_layout(showlegend=False, xaxis_title="Motivo", yaxis_title="Nº de vagas")
        st.plotly_chart(fig_just, use_container_width=True)
    else:
        st.info("Nenhuma justificativa registrada para o filtro selecionado.")

st.markdown(
    """
    **Insight (edite):** esse é um dos dados mais únicos da sua base — ninguém
    mais tem essa informação. Aponte o motivo mais comum de recusa e o que
    isso te diz sobre como focar sua busca (ex: local, horário, stack).
    """
)

st.markdown("---")

# ---------------- Pergunta 4: nicho de mercado ----------------
st.subheader("4. De quais nichos são as vagas encontradas?")
dist_nicho = df_filtrado["Nicho de Mercado"].value_counts()
fig_nicho = px.bar(
    dist_nicho, labels={"value": "Nº de vagas", "index": "Nicho"},
    template=TEMPLATE_GRAFICO,
)
fig_nicho.update_layout(showlegend=False, xaxis_title="Nicho de mercado", yaxis_title="Nº de vagas")
st.plotly_chart(fig_nicho, use_container_width=True)

st.markdown("---")

# ---------------- Tabela detalhada ----------------
st.subheader("Base de dados detalhada")
colunas_exibir = [
    c for c in [
        "Nome da Vaga", "Nome da Empresa", "Nicho de Mercado", "Salário",
        "Benefícios", "Tecnologias Obrigatórias", "Carga Horaria",
        "Tipo de Trabalho", "Interessante pra mim?", "Justificativa",
    ] if c in df_filtrado.columns
]
st.dataframe(df_filtrado[colunas_exibir], use_container_width=True, hide_index=True)

st.caption(
    "⚠️ Vários valores de salário estão como 'Não divulgado' — considere isso "
    "ao interpretar qualquer estatística salarial, ou complemente a base "
    "pesquisando faixas salariais médias de mercado para o cargo."
)
