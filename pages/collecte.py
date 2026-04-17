import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

st.markdown("## Collecte de donnees patients")
st.markdown("---")

tabs = st.tabs(["Saisie manuelle", "Import CSV/Excel", "Donnees depuis URL", "Generation synthetique"])

        st.success(f"Patient enregistre ! IMC : {imc} ({statut_imc}) | Risque : {niveau_risque}")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("IMC calcule", imc, statut_imc)
        col_b.metric("Niveau de risque", niveau_risque)
        col_c.metric("Score de risque", f"{risque}/7")

with tabs[1]:
    st.markdown("### Import de fichier CSV ou Excel")
    fichier_upload = st.file_uploader("Choisir un fichier", type=["csv", "xlsx", "xls"])
    if fichier_upload:
        if fichier_upload.name.endswith(".csv"):
            df_import = pd.read_csv(fichier_upload)
        else:
            df_import = pd.read_excel(fichier_upload)
        st.dataframe(df_import.head(10), use_container_width=True)
        st.info(f"{len(df_import)} lignes importees, {len(df_import.columns)} colonnes")
        if st.button("Sauvegarder ces donnees", type="primary"):
            os.makedirs("data", exist_ok=True)
            df_import.to_csv("data/health_data.csv", index=False)
            st.success("Donnees sauvegardees avec succes !")

with tabs[2]:
    st.markdown("### Chargement depuis une URL")
    url = st.text_input("Entrer l URL du fichier CSV")
    if st.button("Charger depuis URL"):
        try:
            df_url = pd.read_csv(url)
            st.dataframe(df_url.head(10), use_container_width=True)
            st.info(f"{len(df_url)} lignes chargees")
            if st.button("Sauvegarder", key="save_url"):
                df_url.to_csv("data/health_data.csv", index=False)
                st.success("Sauvegarde avec succes !")
        except Exception as e:
            st.error(f"Erreur de chargement : {e}")

with tabs[3]:
    st.markdown("### Generation de donnees synthetiques")
    n = st.slider("Nombre de patients a generer", 50, 1000, 200)
    if st.button("Generer les donnees", type="primary"):
        np.random.seed(42)
        ages = np.random.randint(18, 80, n)
        poids = np.random.normal(72, 15, n).clip(40, 180)
        tailles = np.random.normal(168, 12, n).clip(140, 210)
        imc = (poids / (tailles / 100) ** 2).round(2)
        sexes = np.random.choice(["Homme", "Femme"], n)
        fumeurs = np.random.choice(["Non", "Oui"], n, p=[0.7, 0.3])
        activites = np.random.choice(["Sedentaire", "Moderee", "Intense"], n, p=[0.4, 0.4, 0.2])
        tension_sys = np.random.normal(125, 20, n).clip(80, 220).astype(int)
        tension_dia = np.random.normal(80, 12, n).clip(50, 130).astype(int)
        glycemie = np.random.normal(1.05, 0.3, n).clip(0.6, 4.0).round(2)
        cholesterol = np.random.normal(1.9, 0.4, n).clip(0.8, 4.0).round(2)
        fc = np.random.normal(75, 12, n).clip(45, 180).astype(int)
        diabete = np.random.choice(["Non", "Oui"], n, p=[0.85, 0.15])
        antecedents = np.random.choice(["Non", "Oui"], n, p=[0.8, 0.2])

        # Calcul niveau de risque
        niveau_risque = []
        for i in range(n):
            score = 0
            if tension_sys[i] > 140: score += 1
            if glycemie[i] > 1.26: score += 1
            if cholesterol[i] > 2.0: score += 1
            if fumeurs[i] == "Oui": score += 1
            if antecedents[i] == "Oui": score += 2
            if ages[i] > 60: score += 1
            if score <= 1:
                niveau_risque.append("Faible")
            elif score <= 3:
                niveau_risque.append("Modere")
            else:
                niveau_risque.append("Eleve")

        statut_imc = []
        for val in imc:
            if val < 18.5:
                statut_imc.append("Sous-poids")
            elif val < 25:
                statut_imc.append("Normal")
            elif val < 30:
                statut_imc.append("Surpoids")
            else:
                statut_imc.append("Obesite")

        df_synth = pd.DataFrame({
            "nom": [f"Patient_{i+1}" for i in range(n)],
            "age": ages, "sexe": sexes,
            "poids": poids.round(1), "taille": tailles.round(1), "imc": imc,
            "statut_imc": statut_imc,
            "tension_systolique": tension_sys, "tension_diastolique": tension_dia,
            "glycemie": glycemie, "cholesterol": cholesterol,
            "frequence_cardiaque": fc,
            "fumeur": fumeurs, "activite_physique": activites,
            "diabete": diabete, "antecedents_cardiaques": antecedents,
            "niveau_risque": niveau_risque,
            "date_saisie": str(datetime.today().date())
        })

        df_synth.to_csv("data/health_data.csv", index=False)
        st.success(f"{n} patients generes et sauvegardes !")
        st.dataframe(df_synth.head(10), use_container_width=True)

st.markdown("---")
st.markdown("### Base de donnees actuelle")
if os.path.exists("data/health_data.csv"):
    df = pd.read_csv("data/health_data.csv")
    st.dataframe(df, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total patients", len(df))
    with col2:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Telecharger les donnees", csv, "health_data.csv", "text/csv")
else:
    st.info("Aucune donnee enregistree pour le moment.")
