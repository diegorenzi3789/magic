import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SOS Master Deckbuilder", layout="wide")

# 1. BANCO DE DADOS EXPANDIDO (SOS SET)
@st.cache_data
def get_full_database():
    data = [
        # --- WHITE ---
        {"nome": "Daydream", "cor": "Branco", "cmc": 1, "tier": "B", "faculdade": "Silverquill"},
        {"nome": "Leonin Lightscribe", "cor": "Branco", "cmc": 2, "tier": "A", "faculdade": "Silverquill"},
        {"nome": "Mila, Crafty Companion", "cor": "Branco", "cmc": 3, "tier": "A", "faculdade": "Neutral"},
        
        # --- BLUE ---
        {"nome": "Archmage Emeritus", "cor": "Azul", "cmc": 4, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Solve the Equation", "cor": "Azul", "cmc": 3, "tier": "B", "faculdade": "Quandrix"},
        
        # --- BLACK ---
        {"nome": "Professor Onyx", "cor": "Preto", "cmc": 6, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Baleful Mastery", "cor": "Preto", "cmc": 4, "tier": "A", "faculdade": "Witherbloom"},
        
        # --- RED ---
        {"nome": "Crackle with Power", "cor": "Vermelho", "cmc": 5, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Grinning Ignus", "cor": "Vermelho", "cmc": 3, "tier": "B", "faculdade": "Lorehold"},
        
        # --- GREEN ---
        {"nome": "Ecological Appreciation", "cor": "Verde", "cmc": 4, "tier": "A", "faculdade": "Quandrix"},
        {"nome": "Cultivate", "cor": "Verde", "cmc": 3, "tier": "A", "faculdade": "Arquivo"},
        
        # --- MULTICOLOR (FACULDADES) ---
        {"nome": "Velomachus Lorehold", "cor": "Boros", "cmc": 7, "tier": "S", "faculdade": "Lorehold"},
        {"nome": "Galazeth Prismari", "cor": "Izzet", "cmc": 4, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Beledros Witherbloom", "cor": "Golgari", "cmc": 7, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Shadrix Silverquill", "cor": "Orzhov", "cmc": 5, "tier": "S", "faculdade": "Silverquill"},
        {"nome": "Tanazir Quandrix", "cor": "Simic", "cmc": 5, "tier": "S", "faculdade": "Quandrix"},
        {"nome": "Dina, Soul Steeper", "cor": "Golgari", "cmc": 2, "tier": "B", "faculdade": "Witherbloom"},
        {"nome": "Killian, Ink Duelist", "cor": "Orzhov", "cmc": 2, "tier": "A", "faculdade": "Silverquill"},
        {"nome": "Rootha, Mercurial Artist", "cor": "Izzet", "cmc": 3, "tier": "A", "faculdade": "Prismari"},
        {"nome": "Zimone, Quandrix Prodigy", "cor": "Simic", "cmc": 2, "tier": "B", "faculdade": "Quandrix"},
    ]
    return pd.DataFrame(data)

if 'pool' not in st.session_state:
    st.session_state.pool = []

db = get_full_database()

st.title("🧙‍♂️ SOS Master: Prerelease Helper")

st.header("1. Monte sua Pool")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Buscar na Lista SOS")
    nome_busca = st.selectbox("Selecione a carta:", [""] + sorted(db['nome'].tolist()))
    if st.button("Adicionar da Lista ➕") and nome_busca != "":
        # CORREÇÃO DO ERRO AQUI:
        carta_row = db[db['nome'] == nome_busca].iloc
        st.session_state.pool.append(carta_row.to_dict())
        st.toast(f"{nome_busca} adicionada!")

with col2:
    st.subheader("Não achou a carta?")
    with st.expander("Adicionar Manualmente"):
        m_nome = st.text_input("Nome")
        m_cor = st.selectbox("Cor", ["Branco", "Azul", "Preto", "Vermelho", "Verde", "Multicolor"])
        m_cmc = st.number_input("Custo", 0, 10, 2)
        m_tier = st.select_slider("Poder", ["S", "A", "B", "C", "D"], value="C")
        if st.button("Salvar Carta ✅"):
            st.session_state.pool.append({"nome": m_nome, "cor": m_cor, "cmc": m_cmc, "tier": m_tier, "faculdade": "Manual"})
            st.success("Adicionada!")

if st.session_state.pool:
    df_pool = pd.DataFrame(st.session_state.pool)
    st.divider()
    
    c1, c2 = st.columns()
    with c1:
        st.subheader("Sua Seleção")
        st.table(df_pool[['nome', 'cor', 'cmc', 'tier']])
        if st.button("🗑️ Resetar Tudo"):
            st.session_state.pool = []
            st.rerun()
    with c2:
        st.subheader("Curva de Mana")
        fig, ax = plt.subplots()
        df_pool['cmc'].value_counts().sort_index().plot(kind='bar', ax=ax, color='teal')
        st.pyplot(fig)
