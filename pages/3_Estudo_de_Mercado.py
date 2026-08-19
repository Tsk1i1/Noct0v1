import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from scipy import stats

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

with st.sidebar:
    st.caption(
        "🎨 Trocou o tema agora? Os gráficos Plotly só recalculam a cor "
        "quando a página roda de novo, então clique aqui embaixo em vez "
        "de esperar."
    )
    if st.button("🔄 Sincronizar cores dos gráficos"):
        st.rerun()


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


def mostrar_grafico(fig):
    """Estiliza e renderiza uma figura Plotly, ocupando a largura disponível."""
    st.plotly_chart(estilizar(fig), use_container_width=True)


def formatar_reais(valor: float) -> str:
    """Formata um número no padrão brasileiro (R$ 1.663,64), não no americano."""
    return f"{valor:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")


st.title("📊 Estudo de Mercado: Vagas de Estágio em TI")

# ============================================================
# INTRODUÇÃO
# ============================================================
st.markdown(
    """
    ### Por que este tema

    Escolhi analisar vagas de estágio em Tecnologia da Informação porque é
    exatamente o que estou buscando agora. Em vez de estudar um mercado
    abstrato, resolvi tratar minha própria busca de estágio como um
    problema de dados. Cada vaga que encontrei durante a procura foi
    registrada manualmente com as mesmas informações: tecnologias
    exigidas, tipo de trabalho, benefícios, nicho da empresa e se a vaga me
    interessa ou não, com o motivo quando não interessa. O resultado é uma
    base pequena, mas real e pessoal, que posso usar pra guiar decisões
    concretas: em quais tecnologias focar meus estudos, que tipo de vaga
    vale mais a pena buscar e por que estou recusando as vagas que recuso.
    """
)

df_bruto = carregar_dados()

# ============================================================
# METODOLOGIA
# ============================================================
with st.expander("📋 Metodologia: quais vagas entram nesta análise", expanded=False):
    total_bruto = len(df_bruto)
    total_estagio = int((df_bruto["Tipo da Vaga"] == "Estágio").sum())
    excluidas = total_bruto - total_estagio
    total_com_salario = int(df_bruto["Salário"].notna().sum())

    st.markdown(
        f"""
        A base bruta tem **{total_bruto} registros**, mas nem todos são
        vagas de estágio: {excluidas} são oportunidades de CLT/PJ que
        apareceram na busca e foram guardadas como referência de mercado,
        fora do escopo principal do estudo. Por padrão, as análises abaixo
        consideram só as **{total_estagio} vagas de estágio**; use a opção
        na sidebar se quiser incluir as demais.

        Antes de analisar, também tratei os dados pra evitar contagens
        erradas:
        - Padronizei categorias que estavam digitadas de formas diferentes,
          como "Muito longe" e "Muito Longe", ou "IA" e "Ia", que antes
          eram contadas como coisas separadas.
        - Tratei "Não divulgado" como dado ausente de verdade, não como
          texto, pra não distorcer as contagens.
        - Só {total_com_salario} das {total_bruto} vagas divulgam salário.
          É pouco, mas já dá pra calcular média e intervalo de confiança
          com uma margem de erro honesta em vez de descartar o dado por
          completo; os detalhes estão na pergunta 7.
        """
    )

incluir_clt_pj = st.sidebar.checkbox(
    "Incluir vagas CLT/PJ (fora do escopo de estágio)", value=False
)
df = df_bruto if incluir_clt_pj else df_bruto[df_bruto["Tipo da Vaga"] == "Estágio"]

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
        mostrar_grafico(fig_tec)
    else:
        st.info("Nenhuma tecnologia registrada para o filtro selecionado.")

if not freq_tec.empty:
    top3 = freq_tec.head(3)
    lista_top3 = ", ".join(f"**{t}** ({n} vagas)" for t, n in top3.items())
    st.markdown(
        f"**Observação:** as tecnologias mais exigidas são {lista_top3}. "
        f"SQL e Python aparecem cedo o suficiente na lista pra dizer que "
        f"praticamente viraram pré-requisito de estágio em TI, "
        f"independente da área da empresa. Vale priorizar os dois nos "
        f"estudos."
    )

st.markdown("---")

# ============================================================
# 2. Tipo de trabalho e taxa de recusa
# ============================================================
st.subheader("2. Como se distribuem os tipos de trabalho, e presencial é mais recusado?")
col_c, col_d = st.columns(2)

with col_c:
    dist_tipo = df_filtrado["Tipo de Trabalho"].value_counts()
    fig_tipo = px.pie(values=dist_tipo.values, names=dist_tipo.index, hole=0.4)
    mostrar_grafico(fig_tipo)

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
        mostrar_grafico(fig_recusa)

if "Interessante" in df_filtrado.columns and not df_filtrado.empty and not recusa_por_tipo.empty:
    pior = recusa_por_tipo.index[0]
    pior_valor = recusa_por_tipo.iloc[0]

    grupo_pior = df_filtrado[df_filtrado["Tipo de Trabalho"] == pior]
    n_pior = len(grupo_pior)
    recusadas_pior = int((~grupo_pior["Interessante"]).sum())
    motivos_pior = grupo_pior[grupo_pior["Interessante"] == False]["Justificativa"].dropna()
    motivo_dominante_pior = motivos_pior.value_counts().index[0] if not motivos_pior.empty else None

    texto_obs2 = (
        f"**Observação:** vagas do tipo **{pior}** têm a maior taxa de "
        f"recusa nesta amostra ({pior_valor:.0f}%), mas esse número "
        f"merece uma ressalva. São só {n_pior} vagas desse tipo entre as "
        f"analisadas, e bastaram {recusadas_pior} recusas pra empurrar a "
        f"porcentagem pra cima. Com uma base tão pequena, um número "
        f"pequeno de casos muda o percentual inteiro; se uma dessas vagas "
        f"tivesse me interessado, a taxa cairia bastante."
    )
    if motivo_dominante_pior:
        texto_obs2 += (
            f" Olhando o motivo dessas recusas, a maioria foi por "
            f"{motivo_dominante_pior.lower()}, não porque o formato de "
            f"trabalho em si seja ruim. Continuo preferindo formatos mais "
            f"flexíveis como híbrido e remoto na minha busca; esse número "
            f"alto reflete mais o tamanho pequeno da amostra por tipo do "
            f"que uma rejeição real ao modelo de trabalho."
        )
    st.markdown(texto_obs2)

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
    mostrar_grafico(fig_comp)

    diferenca_por_tecnologia = comparativo["Não interessa"] - comparativo["Interessa"]
    if not diferenca_por_tecnologia.empty and diferenca_por_tecnologia.max() > 0:
        tec_desequilibrio = diferenca_por_tecnologia.idxmax()
        st.markdown(
            f"**Observação:** **{tec_desequilibrio}** aparece bem mais nas "
            f"vagas que não me interessam do que nas que interessam. É "
            f"sinal de que, mesmo sendo comum no mercado, essa tecnologia "
            f"sozinha não é o que decide se uma vaga é boa pra mim: o tipo "
            f"de trabalho e o nicho pesam mais nessa escolha."
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
        mostrar_grafico(fig_just)

        motivo_principal = contagem_just.index[0]
        pct_principal = contagem_just.iloc[0] / justificativas.shape[0] * 100
        st.markdown(
            f"**Observação:** o motivo de recusa mais comum é "
            f"{motivo_principal.lower()}, respondendo por "
            f"{pct_principal:.0f}% das recusas com justificativa "
            f"registrada. Isso é revelador quando junto com o gráfico "
            f"anterior: mesmo entre vagas híbridas, que em teoria deveriam "
            f"facilitar a rotina, o motivo de recusa continua sendo "
            f"majoritariamente ligado a horário ou distância, não à "
            f"tecnologia exigida. Ou seja, o problema não é achar vaga com "
            f"o formato de trabalho certo, é achar vaga com horário e "
            f"localização compatíveis com a minha rotina atual. Esse tipo "
            f"de barreira só aparece porque registrei minhas próprias "
            f"recusas; uma comparação genérica de mercado não capturaria "
            f"isso."
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
mostrar_grafico(fig_nicho)

if not dist_nicho.empty:
    nicho_top = dist_nicho.index[0]
    st.markdown(
        f"**Observação:** **{nicho_top}** é o nicho que mais aparece nas "
        f"vagas encontradas. Vale notar que boa parte das vagas de TI não "
        f"vem só de empresas de tecnologia: setores como financeiro e "
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
    mostrar_grafico(fig_benef)

    top_benef = freq_beneficios.index[0]
    st.markdown(
        f"**Observação:** {top_benef} é o benefício mais comum entre as "
        f"vagas, quase sempre junto de Vale Transporte. Não é o primeiro "
        f"critério que eu olho numa vaga (prioridade minha é tecnologia e "
        f"formato de trabalho), mas virou uma espécie de padrão implícito: "
        f"se uma vaga não oferece isso, já fico desconfiado da proposta "
        f"como um todo."
    )
else:
    st.info("Nenhum benefício registrado para o filtro selecionado.")

st.markdown("---")

# ============================================================
# 7. Sobre os salários
# ============================================================
st.subheader("7. E os salários? Qual a média, e o quanto ela varia?")
com_salario = df_filtrado[df_filtrado["Salário"].notna()]
n_salario = len(com_salario)

if n_salario >= 5:
    salarios = com_salario["Salário"]
    media = salarios.mean()
    mediana = salarios.median()
    desvio = salarios.std(ddof=1)
    erro_padrao = desvio / (n_salario ** 0.5)
    ic_baixo, ic_alto = stats.t.interval(0.95, df=n_salario - 1, loc=media, scale=erro_padrao)

    col_e, col_f = st.columns(2)
    with col_e:
        fig_box = px.box(salarios, points="all", labels={"value": "Salário (R$)"})
        fig_box.update_layout(showlegend=False, xaxis_title="", title="Dispersão (box plot)")
        mostrar_grafico(fig_box)
    with col_f:
        fig_ic = px.bar(
            x=["Média salarial"], y=[media],
            error_y=[ic_alto - media],
            labels={"x": "", "y": "Salário (R$)"},
        )
        fig_ic.update_layout(showlegend=False, title="Média com intervalo de confiança de 95%")
        mostrar_grafico(fig_ic)

    media_arredondada = f"{round(media):,}".replace(",", ".")
    st.markdown(
        f"""
        Com {n_salario} vagas divulgando salário nesta amostra, já dá pra
        calcular algo minimamente confiável: a média é **R$
        {formatar_reais(media)}**, a mediana **R$ {formatar_reais(mediana)}**
        e o desvio padrão **R$ {formatar_reais(desvio)}**.

        O gráfico da direita mostra a média com uma barra de erro: essa
        barra é o intervalo de confiança de 95%, de
        **R$ {formatar_reais(ic_baixo)}** a **R$ {formatar_reais(ic_alto)}**.
        Na prática, isso quer dizer que não dá pra confiar num número
        fechado tipo "a bolsa média é R$ {media_arredondada}" com uma
        amostra de só {n_salario} vagas; o mais honesto é dizer que a
        média real do mercado provavelmente está nessa faixa. A faixa
        ainda é larga porque a amostra é pequena, mas deve estreitar
        conforme mais vagas com salário entrarem na base.

        O box plot ao lado mostra a mesma amostra de outro ângulo: dá pra
        ver que os valores estão bem próximos uns dos outros, sem nenhum
        salário muito destoante puxando a média pra cima ou pra baixo.
        """
    )
else:
    st.markdown(
        f"""
        Só {n_salario} de {len(df_filtrado)} vagas divulgam o valor da
        bolsa ou salário abertamente. É pouco demais pra calcular uma
        média ou intervalo de confiança que façam sentido (o ideal é ter
        pelo menos uns 5 valores), então não tem gráfico salarial aqui
        ainda. Conforme mais vagas com salário forem entrando na base,
        esse gráfico aparece automaticamente.
        """
    )

st.markdown(
    f"""
    O que mais me incomoda nisso, e que não dá pra ver num gráfico, é que
    a maioria das vagas ainda não divulga o salário, mas quase todas
    perguntam no formulário de candidatura qual é a minha pretensão
    salarial. Antes de ter esses {n_salario} valores, eu respondia
    praticamente no escuro. Agora pelo menos tenho uma faixa própria pra
    me basear, mesmo que a empresa específica não divulgue nada: isso
    tanto evita que eu peça mais do que a empresa já tinha planejado
    quanto evita que eu aceite menos do que eu poderia ter negociado.
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

    1. **{top1_tec} é a base técnica mais cobrada.** Reforça que continuar
       estudando essa tecnologia, e não só ferramentas mais "chamativas"
       como IA, tem retorno direto em quantidade de vagas elegíveis.
    2. **A logística pesa mais do que eu esperava.** "{motivo_top}" é o
       motivo de recusa mais frequente, à frente até de falta de
       conhecimento técnico, e aparece mesmo em vagas híbridas. Isso muda
       a estratégia de busca: vale mais a pena ampliar o raio geográfico e
       priorizar horários flexíveis do que só acumular mais tecnologias no
       currículo.
    3. **O nicho "{top1_nicho}" concentra as oportunidades**, mas empresas
       de outros setores, como financeiro e energia, também têm vagas
       técnicas reais. Vale não restringir a busca só a empresas "de
       tecnologia" no nome.

    Esse estudo tem uma limitação clara: a amostra é pequena, poucas
    dezenas de vagas, e foi coletada de forma não sistemática, ao longo da
    minha própria busca. Não é uma amostra representativa de todo o
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