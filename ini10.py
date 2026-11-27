from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="INI 10/2011", layout="wide")

BASE_DIR = Path(__file__).parent


def localizar_excel() -> Path:
    """Procura o Excel da INI10 na raiz do projeto e em subpastas."""
    candidatos = [
        #BASE_DIR / "raw_files" / "INI 10_2011_.xlsx",
        BASE_DIR / "INI 10_2011_.xlsx",
    ]
    for caminho in candidatos:
        if caminho.exists():
            return caminho

    # busca flexível: qualquer .xlsx com "ini" no nome, ignorando maiúsculas
    for caminho in BASE_DIR.rglob("*.xlsx"):
        if "ini" in caminho.name.lower():
            return caminho

    arquivos = [str(p.relative_to(BASE_DIR)) for p in BASE_DIR.rglob("*") if p.is_file()]
    st.error("Arquivo Excel da INI 10/2011 não encontrado no repositório.")
    st.write("Arquivos disponíveis no app:", arquivos)
    st.stop()


@st.cache_data
def carregar_dados():
    arquivo = localizar_excel()
    modalidades = pd.read_excel(arquivo, sheet_name="modalidades")
    normas = pd.read_excel(arquivo, sheet_name="normas_correlacionadas")
    return modalidades, normas


df_raw, df_normas_raw = carregar_dados()
