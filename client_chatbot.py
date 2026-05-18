import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbot Stock Client", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f4f7f5 0%, #e8f1ec 100%);
    font-family: Arial, sans-serif;
}

h1 {
    color: #006b3f;
    text-align: center;
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.stTextInput input {
    border-radius: 12px;
    border: 2px solid #00a859;
    padding: 12px;
}

.stSuccess {
    border-left: 6px solid #00a859;
    border-radius: 12px;
}

.stWarning {
    border-left: 6px solid #f4b400;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = "stock.xlsx"
    calcul = pd.read_excel(file_path, sheet_name="Feuille de calcul", header=None)

    produits = calcul.iloc[2, 2:15].tolist()
    stock_actuel = calcul.iloc[4, 2:15].tolist()

    df = pd.DataFrame({
        "Produit": produits,
        "Stock actuel": stock_actuel
    })

    df = df.dropna(subset=["Produit"])
    df["Stock actuel"] = pd.to_numeric(df["Stock actuel"], errors="coerce")

    return df

df = load_data()

st.title("🤖 Chatbot Stock Client")

st.markdown("""
<div style="
background:white;
padding:18px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
text-align:center;">
Bienvenue. Ce chatbot vous informe uniquement sur le stock actuel disponible.
</div>
""", unsafe_allow_html=True)

st.write("")

question = st.text_input("Demandez le stock d’un produit :")

if question:
    question_lower = question.lower()
    produit_trouve = None

    for produit in df["Produit"]:
        if str(produit).lower() in question_lower:
            produit_trouve = produit
            break

    if produit_trouve:
        ligne = df[df["Produit"] == produit_trouve].iloc[0]

        st.success(
            f"Le stock actuel du produit {produit_trouve} est de "
            f"{round(ligne['Stock actuel'], 2)} unités."
        )

    else:
        st.warning(
            "Désolé, ce produit n’a pas été trouvé. Veuillez écrire le nom exact du produit."
        )
