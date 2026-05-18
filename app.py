
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Stock IA - Holcim", layout="wide")

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

st.title("📦 Système intelligent de gestion et suivi des stocks")
st.write("Dashboard, prévision des ruptures, chatbot client et alertes automatiques.")

col1, col2, col3 = st.columns(3)

col1.metric("Stock total", round(df["Stock actuel"].sum(), 2))
col2.metric("Produits en rupture proche", len(df[df["Statut"] == "Rupture proche"]))
col3.metric("Produits à surveiller", len(df[df["Statut"] == "À surveiller"]))

st.subheader("📊 Tableau de bord")
st.dataframe(df, use_container_width=True)

fig1 = px.bar(df, x="Produit", y="Stock actuel", title="Stock actuel par produit")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(df, x="Produit", y="Couverture jours", title="Couverture du stock en jours")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("⚠️ Prévision des ruptures")

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

st.subheader("🔔 Alertes automatiques")

for _, row in df.iterrows():
    if row["Statut"] == "Rupture proche":
        st.error(f"🚨 {row['Produit']} risque une rupture dans {round(row['Couverture jours'], 1)} jours.")
    elif row["Statut"] == "À surveiller":
        st.warning(f"⚠️ {row['Produit']} doit être surveillé.")
    else:
        st.success(f"✅ {row['Produit']} : stock suffisant.")

st.subheader("🤖 Chatbot client")

question = st.text_input("Posez une question sur un produit :")

if question:
    question_lower = question.lower()
    produit_trouve = None

    for produit in df["Produit"]:
        if str(produit).lower() in question_lower:
            produit_trouve = produit
            break

    if produit_trouve:
        ligne = df[df["Produit"] == produit_trouve].iloc[0]

        st.info(
            f"Le produit {produit_trouve} est disponible avec un stock actuel de "
            f"{round(ligne['Stock actuel'], 2)} unités. "
            f"La couverture estimée est de {round(ligne['Couverture jours'], 1)} jours. "
            f"Statut : {ligne['Statut']}."
        )
    else:
        st.info("Veuillez écrire le nom exact du produit présent dans le tableau.")
