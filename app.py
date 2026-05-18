import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.image("HOLCIM_LOGO.png", width=220)
st.markdown("""
<style>
/* Fond général */
.stApp {
    background: linear-gradient(135deg, #f4f7f5 0%, #e8f1ec 100%);
    font-family: 'Arial', sans-serif;
}

/* Titre principal */
h1 {
    color: #006b3f;
    font-weight: 800;
    text-align: center;
    padding: 20px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

/* Sous-titres */
h2, h3 {
    color: #006b3f;
    font-weight: 700;
}

/* Texte intro */
.stMarkdown p {
    font-size: 17px;
}

/* Cartes KPI */
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border-left: 7px solid #00a859;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

/* Valeurs KPI */
[data-testid="stMetricValue"] {
    color: #006b3f;
    font-weight: bold;
}

/* Tableaux */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* Boutons / input */
.stTextInput input {
    border-radius: 12px;
    border: 2px solid #00a859;
    padding: 12px;
}

/* Messages success */
.stSuccess {
    border-left: 6px solid #00a859;
    border-radius: 12px;
}

/* Messages warning */
.stWarning {
    border-left: 6px solid #f4b400;
    border-radius: 12px;
}

/* Messages error */
.stError {
    border-left: 6px solid #d71920;
    border-radius: 12px;
}

/* Messages info */
.stInfo {
    border-left: 6px solid #0072bc;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = "stock.xlsx"

    calcul = pd.read_excel(file_path, sheet_name="Feuille de calcul", header=None)

    produits = calcul.iloc[2, 2:15].tolist()
    conso_moy = calcul.iloc[3, 2:15].tolist()
    stock_actuel = calcul.iloc[4, 2:15].tolist()
    stock_min = calcul.iloc[5, 2:15].tolist()
    stock_securite = calcul.iloc[6, 2:15].tolist()

    df = pd.DataFrame({
        "Produit": produits,
        "Consommation moyenne/jour": conso_moy,
        "Stock actuel": stock_actuel,
        "Stock minimum": stock_min,
        "Stock sécurité": stock_securite
    })

    df = df.dropna(subset=["Produit"])

    df["Consommation moyenne/jour"] = pd.to_numeric(df["Consommation moyenne/jour"], errors="coerce")
    df["Stock actuel"] = pd.to_numeric(df["Stock actuel"], errors="coerce")
    df["Stock minimum"] = pd.to_numeric(df["Stock minimum"], errors="coerce")
    df["Stock sécurité"] = pd.to_numeric(df["Stock sécurité"], errors="coerce")

    df["Couverture jours"] = df["Stock actuel"] / df["Consommation moyenne/jour"]

    df["Statut"] = df["Couverture jours"].apply(
        lambda x: "Rupture proche" if x <= 5 else "À surveiller" if x <= 10 else "Stock suffisant"
    )

    return df

df = load_data()

st.title("Système intelligent de gestion des stocks - Holcim")
st.markdown("""
<div style="
background:white;
padding:20px;
border-radius:18px;
box-shadow:0 4px 15px rgba(0,0,0,0.08);
text-align:center;
font-size:18px;
color:#333;">
Tableau de bord intelligent destiné aux responsables logistiques pour suivre
les niveaux de stock, anticiper les ruptures, surveiller les produits critiques
et faciliter la prise de décision.
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("Stock total", round(df["Stock actuel"].sum(), 2))
col2.metric("Produits en rupture proche", len(df[df["Statut"] == "Rupture proche"]))
col3.metric("Produits à surveiller", len(df[df["Statut"] == "À surveiller"]))

st.subheader("Tableau de bord analytique")

col_graph1, col_graph2 = st.columns(2)

# =========================
# Graphiques Dashboard
# =========================

st.subheader("📊 Tableau de bord analytique")

col_graph1, col_graph2 = st.columns(2)

with col_graph1:

    fig1 = px.bar(
        df,
        x="Produit",
        y="Stock actuel",
        title="Stock actuel par produit",
        color="Stock actuel",
        color_continuous_scale=[
            "#b7e4c7",
            "#74c69d",
            "#40916c",
            "#1b4332"
        ]
    )

    fig1.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_font_size=22,
        title_font_color="#006b3f",
        font=dict(color="#333"),
        xaxis_title="Produit",
        yaxis_title="Stock actuel"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col_graph2:

    fig2 = px.bar(
        df,
        x="Produit",
        y="Couverture jours",
        title="Couverture du stock en jours",
        color="Couverture jours",
        color_continuous_scale=[
            "#d8f3dc",
            "#95d5b2",
            "#52b788",
            "#2d6a4f"
        ]
    )

    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_font_size=22,
        title_font_color="#006b3f",
        font=dict(color="#333"),
        xaxis_title="Produit",
        yaxis_title="Jours"
    )

    st.plotly_chart(fig2, use_container_width=True)


st.subheader(" Prévision des ruptures")

ruptures = df[df["Statut"] == "Rupture proche"]
surveillance = df[df["Statut"] == "À surveiller"]

if not ruptures.empty:
    st.error("Produits avec risque de rupture proche :")
    st.dataframe(ruptures, use_container_width=True)
else:
    st.success("Aucune rupture proche détectée.")

if not surveillance.empty:
    st.warning("Produits à surveiller :")
    st.dataframe(surveillance, use_container_width=True)

st.subheader(" Alertes automatiques")

for _, row in df.iterrows():
    if row["Statut"] == "Rupture proche":
        st.error(f" {row['Produit']} risque une rupture dans {round(row['Couverture jours'], 1)} jours.")
    elif row["Statut"] == "À surveiller":
        st.warning(f" {row['Produit']} doit être surveillé.")
    else:
        st.success(f" {row['Produit']} : stock suffisant.")

# =========================
# Assistant logistique
# =========================

st.subheader(" Assistant logistique Holcim")

st.markdown("""
<div style="
background:white;
padding:15px;
border-radius:15px;
box-shadow:0 4px 10px rgba(0,0,0,0.08);
font-size:16px;">
Cet assistant aide les responsables à consulter rapidement
les informations du stock et les niveaux critiques.
</div>
""", unsafe_allow_html=True)

question = st.text_input(
    "Responsable : posez une question sur un produit"
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

        stock = round(ligne["Stock actuel"], 2)
        couverture = round(ligne["Couverture jours"], 1)
        statut = ligne["Statut"]

        st.success(
            f"""
Produit : {produit_trouve}

Stock actuel : {stock} unités

📅Couverture estimée : {couverture} jours

Statut : {statut}
"""
        )

    else:

        st.warning(
            "Produit introuvable. Veuillez saisir le nom exact du produit."
        )
