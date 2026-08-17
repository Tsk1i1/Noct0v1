import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Permite importar utils/ quando a página roda dentro de pages/
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data_loader import (  # noqa: E402
    beneficios_mais_frequentes,
    carregar_dados,
    tecnologias_mais_frequentes,
    tecnologias_por_interesse,
)
from utils.theme import cores_atuais  # noqa: E402

st.set_page_config(page_title="Estudo de Mercado", page_icon="📊", layout="wide")

CORES = cores_atuais()


def estilizar(fig):
    """Aplica as cores do tema atual a uma figura Plotly (fundo, texto, grade)."""
    fig.update_layout(
        paper_bgcolor=CORES["fundo"],
        plot_bgcolor=CORES["fundo"],
        font_color=CORES["texto"],
        legend_font_color=CORES["texto"],
    )
    fig.update_xaxes(gridcolor=CORES["grade"], zerolinecolor=CORES["grade"])
    fig.update_yaxes(gridcolor=CORES["grade"], zerolinecolor=CORES["grade"])
    return fig


st.title("📊 Estudo de Mercado — Vagas de Estágio em TI")

# ============================================================
# INTRODUÇÃO
# ============================================================
st.markdown(
    """
    ### Por que este tema

    Escolhi analisar **vagas de estágio em Tecnologia da Informação** porque
    é exatamente o que estou buscando agora — em vez de estudar um mercado
    abstrato, decidi tratar minha própria busca de estágio como um problema
    de dados. Cada vaga que encontrei durante a procura foi registrada
    manualmente com as mesmas informações (tecnologias exigidas, tipo de
    trabalho, benefícios, nicho da empresa e se a vaga me interessa ou não,
    com o motivo). O resultado é uma base pequena, mas real e pessoal — que
    eu posso usar pra guiar decisões concretas: em quais tecnologias focar
    meus estudos, que tipo de vaga vale mais a pena buscar, e por que estou
    recusando as vagas que recuso.
    """
)

df_bruto = carregar_dados()

# ============================================================
# METODOLOGIA
# ============================================================
with st.expander("📋 Metodologia — quais vagas entram nesta análise", expanded=False):
    total_bruto = len(df_bruto)
    total_estagio = int((df_bruto["Tipo da Vaga"] == "Estágio").sum())
    excluidas = total_bruto - total_estagio

    st.markdown(
        f"""
        A base bruta tem **{total_bruto} registros**, mas nem todos são
        vagas de **estágio** — {excluidas} são oportunidades de CLT/PJ que
        apareceram na busca e foram guardadas como referência de mercado,
        fora do escopo principal do estudo (que é estágio). Por padrão, as
        análises abaixo consideram só as **{total_estagio} vagas de
        estágio**; use a opção na sidebar se quiser incluir as demais.

        Outros tratamentos aplicados aos dados antes da análise:
        - **Padronização de categorias digitadas de forma diferente** — por
          exemplo, "Muito longe" e "Muito Longe", ou "IA" e "Ia", eram
          contadas como coisas diferentes até serem unificadas.
        - **"Não divulgado" tratado como dado ausente de verdade** (não como
          texto), pra não distorcer contagens.
        - **Só 2 das {total_bruto} vagas divulgam salário** — por isso não
          há um gráfico de estatística salarial: a amostra é pequena demais
          pra qualquer média ou mediana ser confiável. Trato isso como uma
          observação qualitativa mais adiante, não como número.
        """
    )

incluir_clt_pj = st.sidebar.checkbox(
    "Incluir vagas CLT/PJ (fora do escopo de estágio)", value=False
)
df = df_bruto if incluir_clt_pj else df_bruto[df_bruto["Tipo da Vaga"] == "Estágio"]

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

# ============================================================
# 1. Tecnologias mais exigidas
# ============================================================
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
        )
        fig_tec.update_layout(showlegend=False, yaxis_title="", xaxis_title="Nº de vagas")
        st.plotly_chart(estilizar(fig_tec), use_container_width=True)
    else:
        st.info("Nenhuma tecnologia registrada para o filtro selecionado.")

if not freq_tec.empty:
    top3 = freq_tec.head(3)
    lista_top3 = ", ".join(f"**{t}** ({n} vagas)" for t, n in top3.items())
    st.markdown(
        f"**Observação:** as tecnologias mais exigidas são {lista_top3}. "
        f"SQL e Python aparecem tão cedo na lista que dá pra dizer que são "
        f"praticamente pré-requisito pra estágio de TI hoje, independente "
        f"da área da empresa — vale priorizar esses dois nos estudos."
    )

st.markdown("---")

# ============================================================
# 2. Tipo de trabalho e taxa de recusa
# ============================================================
st.subheader("2. Como se distribuem os tipos de trabalho — e presencial é mais recusado?")
col_c, col_d = st.columns(2)

with col_c:
    dist_tipo = df_filtrado["Tipo de Trabalho"].value_counts()
    fig_tipo = px.pie(values=dist_tipo.values, names=dist_tipo.index, hole=0.4)
    st.plotly_chart(estilizar(fig_tipo), use_container_width=True)

with col_d:
    if "Interessante" in df_filtrado.columns and not df_filtrado.empty:
        recusa_por_tipo = (
            df_filtrado.groupby("Tipo de Trabalho")["Interessante"]
            .apply(lambda s: (~s).mean() * 100)
            .round(1)
            .sort_values(ascending=False)
        )
        fig_recusa = px.bar(
            recusa_por_tipo,
            labels={"value": "% de vagas recusadas", "index": "Tipo de trabalho"},
        )
        fig_recusa.update_layout(showlegend=False, xaxis_title="", yaxis_title="% recusadas")
        st.plotly_chart(estilizar(fig_recusa), use_container_width=True)

if "Interessante" in df_filtrado.columns and not df_filtrado.empty and not recusa_por_tipo.empty:
    pior = recusa_por_tipo.index[0]
    pior_valor = recusa_por_tipo.iloc[0]
    st.markdown(
        f"**Observação:** vagas **{pior}** têm a maior taxa de recusa "
        f"({pior_valor:.0f}%) — ou seja, o tipo de trabalho realmente pesa "
        f"na hora de eu decidir se uma vaga me interessa, não é só a "
        f"tecnologia exigida. Isso sugere que vale a pena filtrar buscas "
        f"futuras priorizando híbrido/remoto, quando possível."
    )

st.markdown("---")

# ============================================================
# 3. Tecnologias: vagas de interesse x vagas recusadas
# ============================================================
st.subheader("3. As vagas que me interessam pedem tecnologias diferentes das que não interessam?")
comparativo = tecnologias_por_interesse(df_filtrado)
if not comparativo.empty:
    comparativo_long = comparativo.reset_index().melt(
        id_vars="Tecnologias_Lista", var_name="Grupo", value_name="Nº de vagas"
    )
    fig_comp = px.bar(
        comparativo_long, x="Tecnologias_Lista", y="Nº de vagas", color="Grupo",
        barmode="group",
    )
    fig_comp.update_layout(xaxis_title="", legend_title="")
    st.plotly_chart(estilizar(fig_comp), use_container_width=True)

    # tecnologia com maior desequilíbrio a favor de "não interessa"
    diff = (comparativo["Não interessa"] - comparativo["Interessa"])
    if not diff.empty and diff.max() > 0:
        tec_desequilibrio = diff.idxmax()
        st.markdown(
            f"**Observação:** **{tec_desequilibrio}** aparece bem mais nas "
            f"vagas que **não** me interessam do que nas que interessam — "
            f"um sinal de que, mesmo sendo uma tecnologia comum no mercado, "
            f"ela sozinha não é o que define se uma vaga é boa pra mim; o "
            f"tipo de trabalho e o nicho pesam mais nessa decisão."
        )
else:
    st.info("Sem dados suficientes para comparar com o filtro selecionado.")

st.markdown("---")

# ============================================================
# 4. Motivos de recusa
# ============================================================
st.subheader("4. Quando uma vaga não me interessa, por quê?")
if "Justificativa" in df_filtrado.columns:
    justificativas = df_filtrado["Justificativa"].dropna()
    if not justificativas.empty:
        contagem_just = justificativas.value_counts()
        fig_just = px.bar(contagem_just)
        fig_just.update_layout(showlegend=False, xaxis_title="Motivo", yaxis_title="Nº de vagas")
        st.plotly_chart(estilizar(fig_just), use_container_width=True)

        motivo_principal = contagem_just.index[0]
        pct_principal = contagem_just.iloc[0] / justificativas.shape[0] * 100
        st.markdown(
            f"**Observação:** o motivo de recusa mais comum é **"
            f"{motivo_principal.lower()}**, respondendo por "
            f"{pct_principal:.0f}% das recusas com justificativa. É um dado "
            f"só meu — mostra que a maior barreira não é falta de "
            f"conhecimento técnico, é logística (horário/local), o que é "
            f"mais fácil de contornar ampliando a busca por vagas remotas "
            f"ou híbridas."
        )
    else:
        st.info("Nenhuma justificativa registrada para o filtro selecionado.")

st.markdown("---")

# ============================================================
# 5. Nicho de mercado
# ============================================================
st.subheader("5. De quais nichos são as vagas encontradas?")
dist_nicho = df_filtrado["Nicho de Mercado"].value_counts()
fig_nicho = px.bar(dist_nicho, labels={"value": "Nº de vagas", "index": "Nicho"})
fig_nicho.update_layout(showlegend=False, xaxis_title="Nicho de mercado", yaxis_title="Nº de vagas")
st.plotly_chart(estilizar(fig_nicho), use_container_width=True)

if not dist_nicho.empty:
    nicho_top = dist_nicho.index[0]
    st.markdown(
        f"**Observação:** **{nicho_top}** é o nicho que mais aparece nas "
        f"vagas encontradas. Vale notar que boa parte das vagas de TI não "
        f"vem só de empresas de tecnologia — setores como financeiro e "
        f"energia também têm times técnicos internos contratando "
        f"estagiários, o que amplia bastante onde vale procurar."
    )

st.markdown("---")

# ============================================================
# 6. Benefícios mais oferecidos
# ============================================================
st.subheader("6. Quais benefícios mais aparecem nas vagas?")
freq_beneficios = beneficios_mais_frequentes(df_filtrado)
if not freq_beneficios.empty:
    fig_benef = px.bar(
        freq_beneficios.sort_values(ascending=True),
        orientation="h",
        labels={"value": "Nº de vagas", "index": "Benefício"},
    )
    fig_benef.update_layout(showlegend=False, yaxis_title="", xaxis_title="Nº de vagas")
    st.plotly_chart(estilizar(fig_benef), use_container_width=True)

    top_benef = freq_beneficios.index[0]
    st.markdown(
        f"**Observação:** **{top_benef}** é o benefício mais comum entre as "
        f"vagas — junto com Vale Transporte, forma praticamente um "
        f"\"pacote padrão\" que se repete na maioria das ofertas, "
        f"independente do nicho da empresa."
    )
else:
    st.info("Nenhum benefício registrado para o filtro selecionado.")

st.markdown("---")

# ============================================================
# 7. Sobre os salários (observação qualitativa, não gráfico)
# ============================================================
st.subheader("7. E os salários?")
com_salario = df_filtrado[df_filtrado["Salário"].notna()]
st.markdown(
    f"""
    Apenas **{len(com_salario)} de {len(df_filtrado)} vagas** divulgam o
    valor da bolsa/salário abertamente. É uma amostra pequena demais pra
    calcular uma média confiável — por isso não há gráfico salarial aqui.
    Mas o próprio fato de quase nenhuma vaga divulgar isso **é** um achado:
    o mercado de estágio em TI é pouco transparente sobre remuneração,
    o que reforça a importância de perguntar diretamente no processo
    seletivo em vez de assumir uma faixa com base na vaga anunciada.
    """
)
if not com_salario.empty:
    st.dataframe(
        com_salario[["Nome da Empresa", "Nome da Vaga", "Salário", "Nicho de Mercado"]],
        use_container_width=True,
        hide_index=True,
    )

st.markdown("---")

# ============================================================
# CONCLUSÃO
# ============================================================
st.subheader("📌 Conclusão")

top1_tec = freq_tec.index[0] if not freq_tec.empty else "—"
top1_nicho = dist_nicho.index[0] if not dist_nicho.empty else "—"
motivo_top = (
    df_filtrado["Justificativa"].dropna().value_counts().index[0]
    if df_filtrado["Justificativa"].dropna().shape[0] > 0
    else "—"
)

st.markdown(
    f"""
    Olhando os {len(df_filtrado)} registros analisados, três conclusões
    práticas se destacam pra minha própria busca de estágio:

    1. **{top1_tec} é a base técnica mais cobrada** — reforça que continuar
       estudando essa tecnologia (e não só ferramentas mais "chamativas"
       como IA) tem retorno direto em quantidade de vagas elegíveis.
    2. **A logística pesa mais do que eu esperava**: "{motivo_top.lower()}"
       é o motivo de recusa mais frequente, à frente até de "não tenho o
       conhecimento técnico". Isso muda a estratégia de busca: vale mais a
       pena ampliar o raio geográfico e priorizar híbrido/remoto do que
       só acumular mais tecnologias no currículo.
    3. **O nicho "{top1_nicho}" concentra as oportunidades**, mas empresas
       de outros setores (financeiro, energia, logística) também têm vagas
       técnicas reais — vale não restringir a busca só a empresas
       "de tecnologia" no nome.

    Esse estudo tem uma limitação clara: a amostra é pequena (poucas
    dezenas de vagas) e foi coletada de forma não sistemática, ao longo da
    minha própria busca — não é uma amostra representativa de todo o
    mercado, é um retrato da minha experiência de busca até aqui. Ainda
    assim, é dado real o suficiente pra orientar decisões concretas sobre
    onde estudar mais e onde procurar melhor.
    """
)

st.markdown("---")

# ============================================================
# Tabela detalhada
# ============================================================
st.subheader("Base de dados detalhada")
colunas_exibir = [
    c for c in [
        "Nome da Vaga", "Nome da Empresa", "Nicho de Mercado", "Salário",
        "Benefícios", "Tecnologias Obrigatórias", "Carga Horaria",
        "Tipo de Trabalho", "Interessante pra mim?", "Justificativa",
    ] if c in df_filtrado.columns
]
st.dataframe(df_filtrado[colunas_exibir], use_container_width=True, hide_index=True)