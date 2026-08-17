"""
Módulo responsável por carregar e limpar a base de dados de vagas de estágio.
Centralizar a limpeza aqui evita repetir código nas páginas e garante que
todo o dashboard trabalhe sempre com os dados no mesmo formato.
"""

import pandas as pd
import streamlit as st

CAMINHO_BASE = "data/vagas_estagio_ti.xlsx"

# Mapeia variações de escrita para um nome canônico, para não contar
# "IA" e "Ia", ou "Html" e "HTML5", como tecnologias diferentes.
NORMALIZACAO_TECNOLOGIAS = {
    "ia": "IA",
    "html": "HTML5",
    "css": "CSS3",
    "sql": "SQL",
    "aws": "AWS",
    "git": "Git",
}


def _normalizar_tecnologia(nome: str) -> str:
    chave = nome.strip().lower()
    return NORMALIZACAO_TECNOLOGIAS.get(chave, nome.strip())


# Unifica justificativas de recusa que são a mesma coisa escrita de forma
# diferente (ex: "Muito longe" vs "Muito Longe"), pra não fragmentar o
# motivo real em categorias separadas no gráfico.
NORMALIZACAO_JUSTIFICATIVA = {
    "muito longe": "Muito longe",
    "horário incompatível": "Horário incompatível",
    "indisponibilidade de horario": "Horário incompatível",
    "indisponibilidade de horário": "Horário incompatível",
    "não tenho os conhecimentos necessarios.": "Não tenho os conhecimentos necessários",
    "não tenho os conhecimentos necessários.": "Não tenho os conhecimentos necessários",
    "não gosto de webdev.": "Não gosto da área",
}


def _normalizar_justificativa(texto: str) -> str:
    if pd.isna(texto):
        return texto
    chave = str(texto).strip().lower()
    return NORMALIZACAO_JUSTIFICATIVA.get(chave, str(texto).strip())


def _normalizar_beneficio(nome: str) -> str:
    """Agrupa grafias diferentes do mesmo benefício sob um nome único."""
    chave = nome.strip().rstrip(".").strip().lower()
    mapa = {
        "vr": "Vale Refeição",
        "va": "Vale Alimentação",
        "vt": "Vale Transporte",
        "plano de saúde": "Plano de Saúde",
        "seguro de vida": "Seguro de Vida",
        "wellhub": "Wellhub/Gympass",
        "gympass": "Wellhub/Gympass",
        "totalpass": "TotalPass",
        "total pass": "TotalPass",
        "bolsa auxilio": "Bolsa Auxílio",
        "bolsa auxílio": "Bolsa Auxílio",
    }
    return mapa.get(chave, nome.strip().rstrip(".").strip())


@st.cache_data
def carregar_dados(caminho: str = CAMINHO_BASE) -> pd.DataFrame:
    """Lê a planilha bruta e devolve um DataFrame já tratado."""
    df = pd.read_excel(caminho)

    # Remove espaços extras nos nomes das colunas (ex: "Carga Horaria " -> "Carga Horaria")
    df.columns = [c.strip() for c in df.columns]

    # Padroniza textos (remove espaços nas pontas)
    colunas_texto = df.select_dtypes(include="object").columns
    for col in colunas_texto:
        df[col] = df[col].astype(str).str.strip()

    # "Não divulgado" e variações viram valor ausente de verdade (NaN),
    # em vez de string, para não quebrar contagens/gráficos e para
    # deixar explícito que a informação não existe.
    df = df.replace(
        to_replace=r"(?i)^não\s*divulgad[oa]$|^nao\s*divulgad[oa]$|^nan$",
        value=pd.NA,
        regex=True,
    )

    # Padroniza "Tipo de Trabalho" (Presencial / Híbrido / Remoto)
    if "Tipo de Trabalho" in df.columns:
        df["Tipo de Trabalho"] = (
            df["Tipo de Trabalho"]
            .str.strip()
            .str.title()
            .replace({"Hibrido": "Híbrido"})
        )

    # Padroniza "Interessante pra mim?" para booleano -> facilita filtros e gráficos
    if "Interessante pra mim?" in df.columns:
        df["Interessante"] = (
            df["Interessante pra mim?"]
            .str.strip()
            .str.lower()
            .map({"sim": True, "não": False, "nao": False})
        )

    # Quebra a coluna de tecnologias (texto livre separado por vírgula)
    # em uma lista, para permitir contar frequência de cada tecnologia.
    if "Tecnologias Obrigatórias" in df.columns:
        df["Tecnologias_Lista"] = (
            df["Tecnologias Obrigatórias"]
            .fillna("")
            .apply(
                lambda x: [
                    _normalizar_tecnologia(t)
                    for t in x.split(",")
                    if t.strip() and t.strip().lower() != "nenhuma"
                ]
            )
        )

    # Unifica justificativas de recusa que descrevem o mesmo motivo mas
    # foram digitadas de forma diferente.
    if "Justificativa" in df.columns:
        df["Justificativa"] = df["Justificativa"].apply(_normalizar_justificativa)

    # Quebra a coluna de benefícios (texto livre separado por vírgula) em
    # lista, agrupando grafias diferentes do mesmo benefício.
    if "Benefícios" in df.columns:
        df["Beneficios_Lista"] = (
            df["Benefícios"]
            .fillna("")
            .apply(
                lambda x: [
                    _normalizar_beneficio(b)
                    for b in x.split(",")
                    if b.strip() and b.strip().lower() != "nenhuma"
                ]
            )
        )

    # Salário como número quando existir (facilita estatísticas descritivas)
    if "Salário" in df.columns:
        df["Salário"] = pd.to_numeric(df["Salário"], errors="coerce")

    return df


def tecnologias_mais_frequentes(df: pd.DataFrame, apenas_interessantes: bool = False) -> pd.Series:
    """Conta a frequência de cada tecnologia exigida nas vagas."""
    base = df[df["Interessante"] == True] if apenas_interessantes else df
    todas = base["Tecnologias_Lista"].explode().dropna()
    return todas.value_counts()


def beneficios_mais_frequentes(df: pd.DataFrame) -> pd.Series:
    """Conta a frequência de cada benefício oferecido nas vagas."""
    todos = df["Beneficios_Lista"].explode().dropna()
    return todos.value_counts()


def tecnologias_por_interesse(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Compara a frequência de cada tecnologia entre vagas que interessam e
    vagas que não interessam — ajuda a identificar se o que te interessa
    pede um conjunto de tecnologias diferente do que não interessa.
    """
    freq_sim = tecnologias_mais_frequentes(df[df["Interessante"] == True])
    freq_nao = tecnologias_mais_frequentes(df[df["Interessante"] == False])
    comparativo = pd.DataFrame({"Interessa": freq_sim, "Não interessa": freq_nao}).fillna(0)
    comparativo["Total"] = comparativo.sum(axis=1)
    comparativo = comparativo.sort_values("Total", ascending=False).head(top_n).drop(columns="Total")
    return comparativo.astype(int)