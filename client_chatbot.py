import streamlit as st
import pandas as pd

# =========================
# Configuration
# =========================

st.set_page_config(
    page_title="Holcim Client Assistant",
    page_icon="🏭",
    layout="centered"
)

# =========================
# Style CSS
# =========================

st.markdown("""
<style>

/* Fond général */
.stApp {
    background: linear-gradient(135deg, #f4f7f5 0%, #e6f4ea 100%);
    font-family: Arial, sans-serif;
}

/* Titre */
h1 {
    color: #006b3f;
    text-align: center;
    font-weight: 800;
}

/* Input */
.stTextInput input {
    border-radius: 14px;
    border: 2px solid #00a859;
    padding: 14px;
    font-size: 16px;
}

/* Success */
.stSuccess {
    border-left: 7px solid #00a859;
    border-radius: 14px;
    background-color: #f0fff5;
}

/* Warning */
.stWarning {
    border-left: 7px solid #f4b400;
    border-radius: 14px;
}

/* Container principal */
.main-card {
    background: white;
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* Texte */
.description {
    text-align: center;
    color: #444;
    font-size: 17px;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Logo
# =========================

st.image("HOLCIM_LOGO.png", width=220)

# =========================
# Titre
# =========================

st.title(" Holcim Stock Assistant")

st.markdown("""
<div class="main-card">

<p class="description">
Bienvenue sur l’assistant client Holcim.
<br><br>
Ce chatbot permet de consulter rapidement
la disponibilité actuelle des produits.
</p>

</div>
""", unsafe_allow_html=True)

# =========================
# Charger les données
# =========================

@st.cache_data
def load_data():

    file_path = "stock.xlsx"

    calcul = pd.read_excel(
        file_path,
        sheet_name="Feuille de calcul",
        header=None
    )

    produits = calcul.iloc[2, 2:15].tolist()
    stock_actuel = calcul.iloc[4, 2:15].tolist()

    df = pd.DataFrame({
        "Produit": produits,
        "Stock actuel": stock_actuel
    })

    df = df.dropna(subset=["Produit"])

    df["Stock actuel"] = pd.to_numeric(
        df["Stock actuel"],
        errors="coerce"
    )

    return df

df = load_data()

# =========================
# Chatbot
# =========================

st.write("")

question = st.text_input(
    "Entrez le nom du produit"
)

if question:

    question_lower = question.lower()
    produit_trouve = None

    for produit in df["Produit"]:

        if str(produit).lower() in question_lower:
            produit_trouve = produit
            break

    if produit_trouve:

        ligne = df[df["Produit"] == produit_trouve].iloc[0]

        stock = round(
            ligne["Stock actuel"],
            2
        )

        st.success(
            f"""
Produit : {produit_trouve}

Stock actuellement disponible :
{stock} unités
"""
        )

    else:

        st.warning(
            """
❌ Produit introuvable.

Veuillez écrire le nom exact du produit.
"""
        )

# =========================
# Footer
# =========================

st.markdown("""
<br><br>

<div style="
text-align:center;
color:#777;
font-size:14px;
">

Holcim Morocco © 2026
<br>
Assistant intelligent de consultation des stocks

</div>
""", unsafe_allow_html=True)
