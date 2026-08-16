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

    # Salário como número quando existir (facilita estatísticas descritivas)
    if "Salário" in df.columns:
        df["Salário"] = pd.to_numeric(df["Salário"], errors="coerce")

    return df


def tecnologias_mais_frequentes(df: pd.DataFrame, apenas_interessantes: bool = False) -> pd.Series:
    """Conta a frequência de cada tecnologia exigida nas vagas."""
    base = df[df["Interessante"] == True] if apenas_interessantes else df
    todas = base["Tecnologias_Lista"].explode().dropna()
    return todas.value_counts()
