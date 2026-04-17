import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da Página
st.set_page_config(page_title="SOS Deck Builder", layout="wide")

# Simulação de Banco de Dados de Secrets of Strixhaven (SOS)
def load_data():
    # Aqui você pode expandir com a lista completa de SOS
    data = [
        {"nome": "Beledros Witherbloom", "cor": "Golgari", "cmc": 7, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Velomachus Lorehold", "cor": "Boros", "cmc": 7, "tier": "S", "faculdade": "Lorehold"},
        {"nome": "Dellian Fel", "cor": "Preto", "cmc": 4, "tier": "S", "faculdade": "Witherbloom"},
        {"nome": "Ral, Guest Lecturer", "cor": "Izzet", "cmc": 3, "tier": "S", "faculdade": "Prismari"},
        {"nome": "Arcane Thesis", "cor": "Azul", "cmc": 2, "tier": "B", "faculdade": "Quandrix"},
        {"nome": "Ink-Tide Leviathan", "cor": "Azul", "cmc": 7, "tier": "A", "faculdade": "Quandrix"},
        {"nome": "Silverquill Command", "cor": "Orzhov", "cmc": 4, "tier": "A", "faculdade": "Silverquill"},
        {"nome": "Lorehold Excavation", "cor": "Boros", "cmc": 2, "tier": "B", "faculdade": "Lorehold"},
        {"nome": "Vortex de Mana", "cor": "Vermelho", "cmc": 1, "tier": "C", "faculdade": "Prismari"},
    ]
    return pd.DataFrame(data)

df_db = load_data()

st.title("🧙‍♂️ Secrets of Strixhaven: Deck Builder")

# --- SESSÃO 1: ADICIONAR CARTAS ---
st.header("1. Sua Pool do Pre-release")
cartas_selecionadas = st.multiselect("Selecione as cartas que você tirou nos boosters:", df_db['nome'].tolist())

if cartas_selecionadas:
    pool_df = df_db[df_db['nome'].isin(cartas_selecionadas)].copy()
    
    # Quantidade de cada carta
    pool_df['qtd'] = 1 # Simplificação para o exemplo
    
    st.subheader("Sua Coleção Organizada")
    st.dataframe(pool_df[['nome', 'cor', 'cmc', 'tier', 'faculdade']], use_container_width=True)

    # --- SESSÃO 2: ANÁLISE ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Curva de Mana")
        fig, ax = plt.subplots()
        pool_df['cmc'].value_counts().sort_index().plot(kind='bar', ax=ax, color='#4CAF50')
        ax.set_xlabel("Custo de Mana")
        ax.set_ylabel("Qtd de Cartas")
        st.pyplot(fig)

    with col2:
        st.subheader("Tier e Sinergia")
        melhor_faculdade = pool_df['faculdade'].mode()
        st.success(f"**Sinergia Principal:** {melhor_faculdade}")
        st.write(f"Cartas de Elite (Tier S/A): {len(pool_df[pool_df['tier'].isin(['S', 'A'])])}")

    # --- SESSÃO 3: IA GENERATOR ---
    st.header("2. IA: Sugestão de Deck Selado (40 cartas)")
    if st.button("Gerar Deck de 40 cartas"):
        # Lógica da IA: Seleciona as melhores cartas e sugere terrenos
        deck_magicas = pool_df.sort_values(by='tier').head(23)
        
        st.write("### Deck Sugerido (23 Mágicas + 17 Terrenos)")
        st.table(deck_magicas[['nome', 'cor', 'cmc']])
        
        st.info("💡 **Dica da IA:** Adicione 17 terrenos (sugestão: 9 de uma cor dominante e 8 da secundária) para fechar as 40 cartas.")

else:
    st.info("Adicione cartas acima para começar a análise.")
