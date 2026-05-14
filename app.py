import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import subprocess

st.set_page_config(
    page_title="SIV Monitor",
    page_icon="🚆",
    layout="wide"
)

st.title("🚆 SIV Monitor")
st.subheader("Dashboard de supervision d’un système d’information voyageurs embarqué")

st.markdown("""
Ce projet simule la supervision d’un système embarqué ferroviaire :  
température, connexion, alimentation, écran voyageurs, GPS et annonces sonores.
""")

if st.button("🔄 Générer de nouvelles données"):
    subprocess.run(["python", "main.py"])
    st.success("Nouvelles données générées avec succès.")

if not os.path.exists("logs_systeme.csv"):
    st.warning("Aucune donnée disponible. Clique sur le bouton pour générer les données.")
    st.stop()

df = pd.read_csv("logs_systeme.csv")

total_tests = len(df)
total_alertes = len(df[df["statut"] == "ALERTE"])
total_ok = len(df[df["statut"] == "OK"])
taux_fiabilite = (total_ok / total_tests) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tests effectués", total_tests)
col2.metric("Systèmes OK", total_ok)
col3.metric("Alertes détectées", total_alertes)
col4.metric("Fiabilité", f"{taux_fiabilite:.2f}%")

st.divider()

st.subheader("📊 Évolution de la température")

fig, ax = plt.subplots()
ax.plot(df["temperature"])
ax.axhline(75, linestyle="--", label="Seuil critique 75°C")
ax.set_xlabel("Test")
ax.set_ylabel("Température °C")
ax.set_title("Température du système embarqué")
ax.legend()
st.pyplot(fig)

st.subheader("🚨 Répartition des statuts")

status_counts = df["statut"].value_counts()

fig2, ax2 = plt.subplots()
ax2.bar(status_counts.index, status_counts.values)
ax2.set_xlabel("Statut")
ax2.set_ylabel("Nombre")
ax2.set_title("OK vs Alertes")
st.pyplot(fig2)

st.divider()

st.subheader("🧾 Derniers logs système")
st.dataframe(df.tail(15), use_container_width=True)

st.subheader("🔍 Alertes détectées")
alertes = df[df["statut"] == "ALERTE"]

if alertes.empty:
    st.success("Aucune alerte détectée.")
else:
    st.dataframe(alertes, use_container_width=True)

st.divider()

st.subheader("📄 Rapport automatique")

if os.path.exists("rapport.txt"):
    with open("rapport.txt", "r", encoding="utf-8") as file:
        st.text(file.read())
else:
    st.info("Rapport non généré.")