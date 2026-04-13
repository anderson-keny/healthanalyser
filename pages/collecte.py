import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

st.markdown("## Collecte de donnees patients")
st.markdown("---")

tabs = st.tabs(["Saisie manuelle", "Import CSV/Excel", "Donnees depuis URL", "Generation synthetique"])

# ============================================================
# ONGLET 1 : SAISIE MANUELLE
# ============================================================
with tabs[0]:
    st.markdown("### Saisie manuelle d un patient")
    col1, col2, col3 = st.columns(3)

    with col1:
        nom = st.text_input("Nom du patient")
        age = st.number_input("Age (ans)", 1, 120, 30)
        sexe = st.selectbox("Sexe", ["Homme", "Femme"])
        poids = st.number_input("Poids (kg)", 10.0, 300.0, 70.0)
        taille = st.number_input("Taille (cm)", 50.0, 250.0, 170.0)

    with col2:
        tension_sys = st.number_input("Tension systolique (mmHg)", 60, 250, 120)
        tension_dia = st.number_input("Tension diastolique (mmHg)", 40, 150, 80)
        glycemie = st.number_input("Glycemie (g/L)", 0.5, 5.0, 1.0)
        cholesterol = st.number_input("Cholesterol (g/L)", 0.5, 5.0, 1.8)
        frequence_cardiaque = st.number_input("Frequence cardiaque (bpm)", 30, 200, 75)

    with col3:
        fumeur = st.selectbox("Fumeur", ["Non", "Oui"])
        activite = st.selectbox("Activite physique", ["Sedentaire", "Moderee", "Intense"])
        diabete = st.selectbox("Diabete", ["Non", "Oui"])
        antecedents = st.selectbox("Antecedents cardiaques", ["Non", "Oui"])
        date_saisie = st.date_input("Date de saisie")

    if st.button("Enregistrer le patient", type="primary"):
        imc = round(poids / ((taille / 100) ** 2), 2)
        if imc < 18.5:
            statut_imc = "Sous-poids"
        elif imc < 25:
            statut_imc = "Normal"
        elif imc < 30:
            statut_imc = "Surpoids"
        else:
            statut_imc = "Obesite"

        risque = 0
        if tension_sys > 140: risque += 1
        if glycemie > 1.26: risque += 1
        if cholesterol > 2.0: risque += 1
        if fumeur == "Oui": risque += 1
        if antecedents == "Oui": risque += 2
        if age > 60: risque += 1
        niveau_risque = "Faible" if risque <= 1 else "Modere" if risque <= 3 else "Eleve"

        nouveau_patient = {
            "nom": nom, "age": age, "sexe": sexe,
            "poids": poids, "taille": taille, "imc": imc, "statut_imc": statut_imc,
            "tension_systolique": tension_sys, "tension_diastolique": tension_dia,
            "glycemie": glycemie, "cholesterol": cholesterol,
            "frequence_cardiaque": frequence_cardiaque,
            "fumeur": fumeur, "activite_physique": activite,
            "diabete": diabete, "antecedents_cardiaques": antecedents,
            "niveau_risque": niveau_risque, "date_saisie": str(date_saisie)
        }

        os.makedirs("data", exist_ok=True)
        fichier = "data/health_data.csv"
        if os.path.exists(fichier):
            df = pd.read_csv(fichier)
            df = pd.concat([df, pd.DataFrame([nouveau_patient])], ignore_index=True)
        else:
            df = pd.DataFrame([nouveau_patient])
        df.to_csv(fichier, index=False)

        st.success(f"Patient enregistre avec succes ! IMC : {imc} ({statut_imc}) | Risque : {niveau_risque}")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("IMC calcule", imc, statut_imc)
        col_b.metric("Niveau de risque", niveau_risque)
        col_c.metric("Score de risque", f"{risque}/7")

# ============================================================
# ONGLET 2 : IMPORT CSV/EXCEL
# ============================================================
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

# ============================================================
# ONGLET 3 : DONNEES DEPUIS URL
# ============================================================
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

# ============================================================
# ONGLET 4 : GENERATION SYNTHETIQUE
# ============================================================
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

        df_synth = pd.DataFrame({
            "nom": [f"Patient_{i+1}" for i in range(n)],
            "age": ages, "sexe": sexes,
            "poids": poids.round(1), "taille": tailles.round(1), "imc": imc,
            "tension_systolique": tension_sys, "tension_diastolique": tension_dia,
            "glycemie": glycemie, "cholesterol": cholesterol,
            "frequence_cardiaque": fc,
            "fumeur": fumeurs, "activite_physique": activites,
            "diabete": diabete, "antecedents_cardiaques": antecedents,
            "date_saisie": str(datetime.today().date())
        })

        df_synth.to_csv("data/health_data.csv", index=False)
        st.success(f"{n} patients generes et sauvegardes !")
        st.dataframe(df_synth.head(10), use_container_width=True)

# ============================================================
# AFFICHAGE BASE DE DONNEES
# ============================================================
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
