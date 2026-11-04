"""Estudo exploratório da busca pessoal por estágio em TI."""

import sys
from pathlib import Path

import plotly.express as px
import streamlit as st
from scipy import stats

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data_loader import (
    beneficios_mais_frequentes,
    carregar_dados,
    tecnologias_mais_frequentes,
    tecnologias_por_interesse,
)
from utils.theme import cores_atuais
from utils.ui import footer, page_header, setup_page

setup_page("Estudo de mercado", "Estudo de mercado")
CORES = cores_atuais()
PALETA = ["#317366", "#8CAA9B", "#BB8D56", "#658599", "#AA7580", "#8C887C"]


def mostrar_grafico(fig):
    """Mantém a identidade dos gráficos e os controles nativos."""
    fig.update_layout(
        paper_bgcolor=CORES["fundo"], plot_bgcolor=CORES["fundo"],
        font={"color": CORES["texto"], "family": "Arial, sans-serif", "size": 13},
        legend_font_color=CORES["texto"],
        margin={"l": 8, "r": 16, "t": 40, "b": 16}, height=360,
    )
    fig.update_xaxes(gridcolor=CORES["grade"], zerolinecolor=CORES["grade"])
    fig.update_yaxes(gridcolor=CORES["grade"], zerolinecolor=CORES["grade"])
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")


def limpar_filtros():
    st.session_state["nicho_mercado"] = []
    st.session_state["tipo_trabalho"] = []


page_header(
    "PROJETO / ANÁLISE DE DADOS", "O que as vagas de estágio pedem?",
    "Uma análise da minha busca por estágio em TI. Tecnologias, formatos de trabalho "
    "e critérios que influenciam quais oportunidades fazem sentido para mim.",
)
df_bruto = carregar_dados()
df = df_bruto.loc[df_bruto["Tipo da Vaga"].eq("Estágio")].copy()

with st.expander("Sobre os dados e a metodologia"):
    st.markdown(
        f"Registrei manualmente **{len(df_bruto)} oportunidades** durante minha busca. "
        f"Este painel considera as **{len(df)} vagas de estágio**; "
        "os demais vínculos ficam fora das análises."
    )
    st.markdown(
        "Padronizei nomes de tecnologias, benefícios e motivos de recusa, "
        "e tratei valores não divulgados como ausentes. A base registra "
        "as exigências das vagas e meu interesse pessoal em cada uma."
    )
    st.caption(
        "A coleta é pessoal e não sistemática. Os resultados descrevem esta base, "
        "sem representar todo o mercado de trabalho."
    )

with st.sidebar:
    st.divider()
    st.subheader("Explorar a base")
    nichos = st.multiselect(
        "Nicho de mercado", sorted(df["Nicho de Mercado"].dropna().unique()),
        key="nicho_mercado", placeholder="Todos os nichos",
    )
    tipos_trabalho = st.multiselect(
        "Tipo de trabalho", sorted(df["Tipo de Trabalho"].dropna().unique()),
        key="tipo_trabalho", placeholder="Todos os formatos",
    )
    st.button("Limpar filtros", on_click=limpar_filtros, width="stretch")
    st.caption("Os filtros atualizam gráficos, indicadores e a tabela de vagas.")

df_filtrado = df.copy()
if nichos:
    df_filtrado = df_filtrado.loc[df_filtrado["Nicho de Mercado"].isin(nichos)]
if tipos_trabalho:
    df_filtrado = df_filtrado.loc[df_filtrado["Tipo de Trabalho"].isin(tipos_trabalho)]

st.caption(f"RECORTE ATUAL · {len(df_filtrado)} de {len(df)} vagas de estágio")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Vagas analisadas", len(df_filtrado))
c2.metric("Empresas", df_filtrado["Nome da Empresa"].nunique())
c3.metric("Vagas de interesse", int(df_filtrado["Interessante"].sum()))
c4.metric("Com salário divulgado", f'{df_filtrado["Salário"].notna().mean() * 100:.0f}%' if len(df_filtrado) else "—")

if df_filtrado.empty:
    st.info("Nenhuma vaga combina com esses filtros. Remova uma seleção ou use ‘Limpar filtros’.")
    footer()
    st.stop()

st.divider()
st.header("01 / Tecnologias exigidas")
st.caption("Quais tecnologias aparecem nas vagas selecionadas?")
apenas_interesse = st.checkbox("Somente vagas do meu interesse", value=False)
freq_tec = tecnologias_mais_frequentes(df_filtrado, apenas_interessantes=apenas_interesse)
if not freq_tec.empty:
    fig = px.bar(freq_tec.sort_values(ascending=True), orientation="h",
                 color_discrete_sequence=PALETA, labels={"value": "Nº de vagas", "index": "Tecnologia"})
    fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="Nº de vagas")
    mostrar_grafico(fig)
    destaques = ", ".join(f"{t} ({n})" for t, n in freq_tec.head(3).items())
    st.markdown(f"As tecnologias mais frequentes neste recorte são **{destaques}**.")
else:
    st.info("Nenhuma tecnologia registrada para a seleção atual.")
st.caption("Uma vaga pode citar mais de uma tecnologia; as contagens não são exclusivas.")

st.divider()
st.header("02 / Formatos de trabalho")
st.caption("Como se distribuem as vagas e quais formatos têm mais recusas pessoais?")
col_a, col_b = st.columns(2)
dist_tipo = df_filtrado["Tipo de Trabalho"].value_counts()
avaliadas = df_filtrado.dropna(subset=["Interessante", "Tipo de Trabalho"])
recusa_por_tipo = (
    avaliadas.groupby("Tipo de Trabalho")["Interessante"]
    .apply(lambda serie: serie.eq(False).mean() * 100).sort_values(ascending=False)
)
with col_a:
    if not dist_tipo.empty:
        fig = px.pie(values=dist_tipo.values, names=dist_tipo.index, hole=0.65, color_discrete_sequence=PALETA)
        fig.update_traces(textinfo="label+percent")
        fig.update_layout(showlegend=False, title="Vagas por formato")
        mostrar_grafico(fig)
    else:
        st.info("Formato de trabalho não informado neste recorte.")
with col_b:
    if not recusa_por_tipo.empty:
        fig = px.bar(recusa_por_tipo, color_discrete_sequence=PALETA,
                     labels={"value": "% de vagas recusadas", "index": "Tipo de trabalho"})
        fig.update_layout(showlegend=False, title="Recusa por formato", xaxis_title="", yaxis_title="% recusadas")
        fig.update_yaxes(range=[0, 100], ticksuffix="%")
        mostrar_grafico(fig)
    else:
        st.info("Sem avaliações de interesse para comparar os formatos.")
if not recusa_por_tipo.empty:
    formato = recusa_por_tipo.index[0]
    grupo = avaliadas.loc[avaliadas["Tipo de Trabalho"].eq(formato)]
    recusadas = int(grupo["Interessante"].eq(False).sum())
    st.markdown(
        f"**{formato}** tem a maior taxa de recusa neste recorte: "
        f"{recusa_por_tipo.iloc[0]:.0f}% ({recusadas} de {len(grupo)} vagas avaliadas). "
        "As recusas refletem meus critérios pessoais; o formato sozinho não explica o motivo."
    )

st.divider()
st.header("03 / Tecnologias e interesse")
st.caption("As vagas que me interessam pedem tecnologias diferentes das demais?")
comparativo = tecnologias_por_interesse(df_filtrado)
if not comparativo.empty:
    comparativo_long = comparativo.rename_axis("Tecnologia").reset_index().melt(
        id_vars="Tecnologia", var_name="Grupo", value_name="Nº de vagas"
    )
    fig = px.bar(comparativo_long, x="Tecnologia", y="Nº de vagas", color="Grupo",
                 barmode="group", color_discrete_sequence=PALETA)
    fig.update_layout(xaxis_title="", legend_title="")
    mostrar_grafico(fig)
    st.caption(
        "Comparação das dez tecnologias mais citadas. Os grupos podem ter tamanhos "
        "diferentes; o gráfico mostra contagens, sem atribuir o interesse à tecnologia."
    )
else:
    st.info("Sem tecnologias suficientes para comparar na seleção atual.")

st.divider()
st.header("04 / Motivos de recusa")
st.caption("Por que algumas vagas não se encaixam na minha busca?")
justificativas = df_filtrado.loc[df_filtrado["Interessante"].eq(False), "Justificativa"].dropna()
contagem_just = justificativas.value_counts()
if not contagem_just.empty:
    fig = px.bar(contagem_just.sort_values(), orientation="h", color_discrete_sequence=PALETA,
                 labels={"value": "Nº de vagas", "index": "Motivo"})
    fig.update_layout(showlegend=False, xaxis_title="Nº de vagas", yaxis_title="")
    mostrar_grafico(fig)
    percentual = contagem_just.iloc[0] / len(justificativas) * 100
    st.markdown(
        f"**{contagem_just.index[0]}** é o motivo mais registrado: "
        f"{contagem_just.iloc[0]} de {len(justificativas)} recusas com justificativa ({percentual:.0f}%)."
    )
else:
    st.info("Nenhuma recusa com justificativa registrada neste recorte.")

st.divider()
st.header("05 / Nichos de mercado")
st.caption("Em quais setores estão as oportunidades encontradas?")
dist_nicho = df_filtrado["Nicho de Mercado"].value_counts()
if not dist_nicho.empty:
    fig = px.bar(dist_nicho.sort_values(), orientation="h", color_discrete_sequence=PALETA,
                 labels={"value": "Nº de vagas", "index": "Nicho"})
    fig.update_layout(showlegend=False, xaxis_title="Nº de vagas", yaxis_title="")
    mostrar_grafico(fig)
    st.markdown(f"**{dist_nicho.index[0]}** reúne o maior número de vagas neste recorte ({dist_nicho.iloc[0]}).")
else:
    st.info("Nenhum nicho informado para a seleção atual.")

st.divider()
st.header("06 / Benefícios oferecidos")
st.caption("Quais benefícios são mencionados nas vagas?")
freq_beneficios = beneficios_mais_frequentes(df_filtrado)
if not freq_beneficios.empty:
    fig = px.bar(freq_beneficios.sort_values(), orientation="h", color_discrete_sequence=PALETA,
                 labels={"value": "Nº de vagas", "index": "Benefício"})
    fig.update_layout(showlegend=False, xaxis_title="Nº de vagas", yaxis_title="")
    mostrar_grafico(fig)
    st.markdown(f"**{freq_beneficios.index[0]}** é o benefício mais citado, presente em {freq_beneficios.iloc[0]} vagas da seleção.")
    st.caption("A ausência de um benefício no anúncio não confirma que ele não seja oferecido.")
else:
    st.info("Nenhum benefício registrado para a seleção atual.")

st.divider()
st.header("07 / Bolsas e salários")
st.caption("Quais valores foram divulgados e como variam?")
com_salario = df_filtrado.loc[df_filtrado["Salário"].notna()]
n_salario = len(com_salario)
if n_salario >= 5:
    salarios = com_salario["Salário"]
    media, mediana, desvio = salarios.mean(), salarios.median(), salarios.std(ddof=1)
    erro_padrao = desvio / n_salario ** 0.5
    ic_baixo, ic_alto = (
        stats.t.interval(0.95, df=n_salario - 1, loc=media, scale=erro_padrao)
        if erro_padrao > 0 else (media, media)
    )
    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.box(salarios, points="all", color_discrete_sequence=PALETA, labels={"value": "Valor mensal (R$)"})
        fig.update_layout(showlegend=False, xaxis_title="", title="Distribuição dos valores")
        mostrar_grafico(fig)
    with col_b:
        fig = px.bar(x=["Média"], y=[media], error_y=[ic_alto - media], color_discrete_sequence=PALETA,
                     labels={"x": "", "y": "Valor mensal (R$)"})
        fig.update_layout(showlegend=False, title="Média e intervalo t de 95%")
        mostrar_grafico(fig)
    st.markdown(
        f"Nas **{n_salario} vagas com valor divulgado**, a média é **{formatar_reais(media)}**, "
        f"a mediana {formatar_reais(mediana)} e o desvio padrão {formatar_reais(desvio)}. "
        f"O intervalo t calculado vai de {formatar_reais(ic_baixo)} a {formatar_reais(ic_alto)}."
    )
else:
    st.info(
        f"{n_salario} de {len(df_filtrado)} vagas informam remuneração. "
        "Este painel exibe os gráficos salariais a partir de cinco valores; "
        "os registros disponíveis podem ser consultados abaixo."
    )
st.caption(
    "O intervalo t é uma exploração estatística dos valores disponíveis. A coleta não aleatória "
    "e a falta de salários em parte dos anúncios impedem generalizá-lo ao mercado."
)
if not com_salario.empty:
    st.dataframe(
        com_salario[["Nome da Empresa", "Nome da Vaga", "Salário", "Nicho de Mercado"]],
        width="stretch", hide_index=True,
        column_config={"Salário": st.column_config.NumberColumn("Valor mensal (R$)", format="%.2f")},
    )

st.divider()
st.header("Leituras do recorte")
freq_resumo = tecnologias_mais_frequentes(df_filtrado)
if not freq_resumo.empty:
    st.markdown(f"- **Tecnologia mais citada:** {freq_resumo.index[0]}, em {freq_resumo.iloc[0]} vagas.")
if not contagem_just.empty:
    st.markdown(f"- **Motivo de recusa mais registrado:** {contagem_just.index[0]}.")
if not dist_nicho.empty:
    st.markdown(f"- **Nicho com mais oportunidades:** {dist_nicho.index[0]}.")
st.caption(
    "Os destaques mostram o primeiro colocado em cada contagem e podem ter empates. "
    "São pistas para minha busca de estágio, limitadas às vagas que registrei."
)

st.divider()
st.header("Base de dados")
st.caption("Consulte os registros do recorte ou baixe uma cópia para explorar os dados.")
colunas_exibir = [
    "Nome da Vaga", "Nome da Empresa", "Nicho de Mercado", "Salário", "Benefícios",
    "Tecnologias Obrigatórias", "Carga Horaria", "Tipo de Trabalho", "Interessante pra mim?", "Justificativa",
]
base_exibir = df_filtrado[colunas_exibir]
st.download_button(
    "Baixar recorte em CSV", data=base_exibir.to_csv(index=False, sep=";").encode("utf-8-sig"),
    file_name="vagas_estagio_recorte.csv", mime="text/csv",
)
st.dataframe(base_exibir, width="stretch", hide_index=True)
footer()
