"""Carrega e limpa a base de vagas de estágio para uso em todo o dashboard."""

import pandas as pd
import streamlit as st

CAMINHO_BASE = "data/vagas_estagio_ti.xlsx"

NORMALIZACAO_TECNOLOGIAS = {
    "ia": "IA",
    "html": "HTML5",
    "css": "CSS3",
    "sql": "SQL",
    "aws": "AWS",
    "git": "Git",
}

NORMALIZACAO_JUSTIFICATIVA = {
    "muito longe": "Muito longe",
    "horário incompatível": "Horário incompatível",
    "indisponibilidade de horario": "Horário incompatível",
    "indisponibilidade de horário": "Horário incompatível",
    "não tenho os conhecimentos necessarios.": "Não tenho os conhecimentos necessários",
    "não tenho os conhecimentos necessários.": "Não tenho os conhecimentos necessários",
    "não gosto de webdev.": "Não gosto da área",
}

NORMALIZACAO_BENEFICIOS = {
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
    "bolsa auxilo": "Bolsa Auxílio",
    "bolsa auxílio": "Bolsa Auxílio",
}


def _normalizar_tecnologia(nome: str) -> str:
    return NORMALIZACAO_TECNOLOGIAS.get(nome.strip().lower(), nome.strip())


def _normalizar_justificativa(texto: str) -> str:
    if pd.isna(texto):
        return texto
    return NORMALIZACAO_JUSTIFICATIVA.get(str(texto).strip().lower(), str(texto).strip())


def _normalizar_beneficio(nome: str) -> str:
    chave = nome.strip().rstrip(".").strip().lower()
    return NORMALIZACAO_BENEFICIOS.get(chave, nome.strip().rstrip(".").strip())


def _quebrar_lista(texto: str, normalizar) -> list:
    """Transforma um campo de texto livre separado por vírgula numa lista normalizada."""
    itens = str(texto).split(",") if pd.notna(texto) else []
    return [normalizar(item) for item in itens if item.strip() and item.strip().lower() != "nenhuma"]


def _remover_espacos_das_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [coluna.strip() for coluna in df.columns]
    return df


def _remover_espacos_dos_textos(df: pd.DataFrame) -> pd.DataFrame:
    colunas_texto = df.select_dtypes(include="object").columns
    for coluna in colunas_texto:
        df[coluna] = df[coluna].astype(str).str.strip()
    return df


def _tratar_nao_divulgado_como_ausente(df: pd.DataFrame) -> pd.DataFrame:
    """'Não divulgado' e variações viram NaN de verdade, não texto, para não distorcer contagens."""
    return df.replace(
        to_replace=r"(?i)^não\s*divulgad[oa]$|^nao\s*divulgad[oa]$|^nan$",
        value=pd.NA,
        regex=True,
    )


def _padronizar_tipo_de_trabalho(df: pd.DataFrame) -> pd.DataFrame:
    if "Tipo de Trabalho" in df.columns:
        df["Tipo de Trabalho"] = (
            df["Tipo de Trabalho"].str.strip().str.title().replace({"Hibrido": "Híbrido"})
        )
    return df


def _converter_interesse_em_booleano(df: pd.DataFrame) -> pd.DataFrame:
    if "Interessante pra mim?" in df.columns:
        df["Interessante"] = (
            df["Interessante pra mim?"].str.strip().str.lower().map({"sim": True, "não": False, "nao": False})
        )
    return df


def _extrair_lista_de_tecnologias(df: pd.DataFrame) -> pd.DataFrame:
    if "Tecnologias Obrigatórias" in df.columns:
        df["Tecnologias_Lista"] = df["Tecnologias Obrigatórias"].apply(
            lambda x: _quebrar_lista(x, _normalizar_tecnologia)
        )
    return df


def _unificar_justificativas_equivalentes(df: pd.DataFrame) -> pd.DataFrame:
    if "Justificativa" in df.columns:
        df["Justificativa"] = df["Justificativa"].apply(_normalizar_justificativa)
    return df


def _extrair_lista_de_beneficios(df: pd.DataFrame) -> pd.DataFrame:
    if "Benefícios" in df.columns:
        df["Beneficios_Lista"] = df["Benefícios"].apply(
            lambda x: _quebrar_lista(x, _normalizar_beneficio)
        )
    return df


def _converter_salario_em_numero(df: pd.DataFrame) -> pd.DataFrame:
    if "Salário" in df.columns:
        df["Salário"] = pd.to_numeric(df["Salário"], errors="coerce")
    return df


@st.cache_data
def carregar_dados(caminho: str = CAMINHO_BASE) -> pd.DataFrame:
    """Lê a planilha bruta e devolve um DataFrame pronto para análise."""
    df = pd.read_excel(caminho)
    df = _remover_espacos_das_colunas(df)
    df = _remover_espacos_dos_textos(df)
    df = _tratar_nao_divulgado_como_ausente(df)
    df = _padronizar_tipo_de_trabalho(df)
    df = _converter_interesse_em_booleano(df)
    df = _extrair_lista_de_tecnologias(df)
    df = _unificar_justificativas_equivalentes(df)
    df = _extrair_lista_de_beneficios(df)
    df = _converter_salario_em_numero(df)
    return df


def tecnologias_mais_frequentes(df: pd.DataFrame, apenas_interessantes: bool = False) -> pd.Series:
    """Conta a frequência de cada tecnologia exigida nas vagas."""
    base = df[df["Interessante"] == True] if apenas_interessantes else df
    return base["Tecnologias_Lista"].explode().dropna().value_counts()


def beneficios_mais_frequentes(df: pd.DataFrame) -> pd.Series:
    """Conta a frequência de cada benefício oferecido nas vagas."""
    return df["Beneficios_Lista"].explode().dropna().value_counts()


def tecnologias_por_interesse(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Compara, lado a lado, a frequência de cada tecnologia entre vagas que interessam e as que não interessam."""
    freq_interessa = tecnologias_mais_frequentes(df[df["Interessante"] == True])
    freq_nao_interessa = tecnologias_mais_frequentes(df[df["Interessante"] == False])
    comparativo = pd.DataFrame(
        {"Interessa": freq_interessa, "Não interessa": freq_nao_interessa}
    ).fillna(0)
    comparativo["Total"] = comparativo.sum(axis=1)
    comparativo = comparativo.sort_values("Total", ascending=False).head(top_n).drop(columns="Total")
    return comparativo.astype(int)
