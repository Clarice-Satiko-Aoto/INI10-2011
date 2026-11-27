from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="INI 10/2011", layout="wide")

BASE_DIR = Path(__file__).parent
ARQUIVO_INI = BASE_DIR / "raw_files" / "INI 10_2011_.xlsx"
ARQUIVO_SP = BASE_DIR / "sp_alvo.csv"


@st.cache_data
def carregar_dados():
    modalidades = pd.read_excel(ARQUIVO_INI, sheet_name="modalidades")
    normas = pd.read_excel(ARQUIVO_INI, sheet_name="normas_correlacionadas")
    return modalidades, normas


df_raw, df_normas_raw = carregar_dados()

st.title("Instrução Normativa Interministerial MPA/MMA nº 10, de 2011")

# --- Filtros ---
st.sidebar.header("Filtros")
especies = sorted(df_raw["Espécie-alvo"].dropna().unique())
sp_selecionado = st.sidebar.selectbox("Espécie-alvo", options=especies)

# --- Modalidades da espécie ---
df_filtrado = df_raw[df_raw["Espécie-alvo"] == sp_selecionado]

st.subheader(f"Modalidade(s) para: {sp_selecionado}")
st.caption(f"{len(df_filtrado)} modalidade(s) encontrada(s)")

# Cada modalidade em um expander, com campo/valor em tabela larga
for _, linha in df_filtrado.iterrows():
    titulo = f"Modalidade {linha['Cod INI10.2011']}"
    with st.expander(titulo, expanded=len(df_filtrado) == 1):
        detalhe = (
            linha.astype(str)
            .rename("Valor")
            .rename_axis("Campo")
            .reset_index()
        )
        st.dataframe(
            detalhe,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Campo": st.column_config.TextColumn("Campo", width="small"),
                "Valor": st.column_config.TextColumn("Valor", width="large"),
            },
        )

# --- Normas correlacionadas ---
st.subheader("Normas correlacionadas")
codigos = df_filtrado["Cod INI10.2011"].unique()
df_normas = df_normas_raw[df_normas_raw["Cod INI10.2011"].isin(codigos)]

if df_normas.empty:
    st.info("Nenhuma norma correlacionada para esta espécie.")
else:
    st.dataframe(
        df_normas.drop(columns=["Data publicacao"], errors="ignore"),
        hide_index=True,
        use_container_width=True,
    )