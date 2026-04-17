import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da Página
st.set_page_config(page_title="SOS Deck Builder 2026", layout="wide")

# BANCO DE DADOS ATUALIZADO: SECRETS OF STRIXHAVEN (SOS)
def load_data():
    data = [
        # --- LOREHOLD (RW) - Flashback ---
        {"nome": "Velomachus Lorehold", "cor": "Boros", "cmc": 7, "tier": "S", "faculdade": "Lorehold"},
        {"nome": "Lorehold, the Historian", "cor": "Boros", "cmc": 5, "tier": "S", "faculdade": "Lorehold"},
        {"nome": "Ennis, Debate Moderator", "cor": "Branco", "cmc": 3, "tier": "A", "faculdade": "Lorehold"},
        
        # --- PRISMARI (UR) - Opus ---
        {"nome": "Galazeth Prismari", "cor": "Izzet", "cmc": 4, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Prismari, the Inspiration", "cor": "Izzet", "cmc": 6, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Ral Zarek, Guest Lecturer", "cor": "Izzet", "cmc": 3, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Spectacular Skywhale", "cor": "Azul", "cmc": 5, "tier": "A", "faculdade": "Prismari"},
        
        # --- WITHERBLOOM (BG) - Infusion ---
        {"nome": "Beledros Witherbloom", "cor": "Golgari", "cmc": 7, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Witherbloom, the Balancer", "cor": "Golgari", "cmc": 4, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Dina's Guidance", "cor": "Verde", "cmc": 2, "tier": "B", "faculdade": "Witherbloom"},
        {"nome": "Bogwater Lumaret", "cor": "Preto", "cmc": 3, "tier": "B", "faculdade": "Witherbloom"},
        
        # --- SILVERQUILL (WB) - Repartee ---
        {"nome": "Shadrix Silverquill", "cor": "Orzhov", "cmc": 5, "tier": "S", "faculdade": "Silverquill"},
        {"nome": "Silverquill, the Disputant", "cor": "Orzhov", "cmc": 4, "tier": "S", "faculdade": "Silverquill"},
        {"nome": "Inkling Mascot", "cor": "Preto", "cmc": 2, "tier": "C", "faculdade": "Silverquill"},
        
        # --- QUANDRIX (UG) - Increment ---
        {"nome": "Tanazir Quandrix", "cor": "Simic", "cmc": 5, "tier": "S", "faculdade": "Quandrix"},
        {"nome": "Quandrix, the Proof", "cor": "Simic", "cmc": 6, "tier": "S", "faculdade": "Quandrix"},
        {"nome": "Jadzi, Steward of Fate", "cor": "Simic", "cmc": 8, "tier": "A", "faculdade": "Quandrix"},
        {"nome": "Applied Geometry", "cor": "Verde", "cmc": 1, "tier": "C", "faculdade": "Quandrix"},
        
        # --- MYSTICAL ARCHIVE (SOA) ---
        {"nome": "Day of Judgment", "cor": "Branco", "cmc": 4, "tier": "S", "faculdade": "Arquivo"},
        {"nome": "Brainstorm", "cor": "Azul", "cmc": 1, "tier": "A", "faculdade": "Arquivo"},
        {"nome": "Dark Ritual", "cor": "Preto", "cmc": 1, "tier": "S", "faculdade": "Arquivo"},
        {"nome": "Lightning Bolt", "cor": "Vermelho", "cmc": 1, "tier": "S", "faculdade": "Arquivo"},
    ]
    # DICA: Adicione aqui as outras comuns que você abrir no kit!
    return pd.DataFrame(data)

df_db = load_data()

st.title("🧙‍♂️ Secrets of Strixhaven (2026): Prerelease Helper")

# BUSCA POR TEXTO (Para facilitar no celular)
st.header("1. Sua Pool")
busca = st.text_input("Digite o nome da carta para filtrar (ex: 'Beledros'):").lower()
opcoes = df_db[df_db['nome'].str.lower().str.contains(busca)]['nome'].tolist()

cartas_selecionadas = st.multiselect("Selecione as cartas da sua pool:", options=opcoes)

if cartas_selecionadas:
    pool_df = df_db[df_db['nome'].isin(cartas_selecionadas)].copy()
    st.dataframe(pool_df[['nome', 'cor', 'cmc', 'tier', 'faculdade']], use_container_width=True)

    # ANÁLISE IA
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Curva de Mana")
        fig, ax = plt.subplots()
        pool_df['cmc'].value_counts().sort_index().plot(kind='bar', ax=ax, color='#7b2cbf')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Sugestão de Deck")
        if len(pool_df) >= 5:
            melhor_facul = pool_df['faculdade'].mode()
            st.success(f"Vá de **{melhor_facul}**! Suas melhores cartas estão lá.")
            if st.button("IA: Gerar Deck Selado"):
                deck = pool_df.sort_values(by='tier').head(23)
                st.table(deck[['nome', 'cmc', 'faculdade']])
