import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.markdown("## Outils medicaux avances")
st.markdown("---")

tabs = st.tabs(["Calculateur IMC avance", "Score de risque cardiovasculaire"])

# ============================================================
# CALCULATEUR IMC AVANCE
# ============================================================
with tabs[0]:
    st.markdown("### Calculateur IMC et morphologie")

    col1, col2 = st.columns(2)
    with col1:
        age_imc = st.number_input("Age", 1, 120, 30, key="age_imc")
        sexe_imc = st.selectbox("Sexe", ["Homme", "Femme"], key="sexe_imc")
        poids_imc = st.number_input("Poids (kg)", 10.0, 300.0, 70.0, key="poids_imc")
        taille_imc = st.number_input("Taille (cm)", 50.0, 250.0, 170.0, key="taille_imc")
        tour_taille = st.number_input("Tour de taille (cm)", 40.0, 200.0, 80.0)
        tour_hanche = st.number_input("Tour de hanche (cm)", 40.0, 200.0, 95.0)

    with col2:
        activite_imc = st.selectbox("Niveau d activite", [
            "Sedentaire", "Legerement actif", "Moderement actif", "Tres actif", "Extremement actif"
        ])
        objectif = st.selectbox("Objectif", [
            "Perte de poids", "Maintien du poids", "Prise de masse"
        ])

    if st.button("Calculer mon profil complet", type="primary"):
        imc = round(poids_imc / ((taille_imc / 100) ** 2), 2)
        rth = round(tour_taille / tour_hanche, 2)

        if imc < 16:
            cat_imc = "Denutrition severe"
            couleur = "#FF0000"
        elif imc < 17:
            cat_imc = "Denutrition moderee"
            couleur = "#FF4500"
        elif imc < 18.5:
            cat_imc = "Sous-poids"
            couleur = "#FFA500"
        elif imc < 25:
            cat_imc = "Poids normal"
            couleur = "#00C851"
        elif imc < 30:
            cat_imc = "Surpoids"
            couleur = "#FFA500"
        elif imc < 35:
            cat_imc = "Obesite moderee"
            couleur = "#FF4500"
        elif imc < 40:
            cat_imc = "Obesite severe"
            couleur = "#FF0000"
        else:
            cat_imc = "Obesite morbide"
            couleur = "#8B0000"

        if sexe_imc == "Homme":
            risque_rth = "Eleve" if rth > 0.9 else "Normal"
        else:
            risque_rth = "Eleve" if rth > 0.85 else "Normal"

        facteurs = {"Sedentaire": 1.2, "Legerement actif": 1.375,
                    "Moderement actif": 1.55, "Tres actif": 1.725, "Extremement actif": 1.9}
        if sexe_imc == "Homme":
            bmr = 88.362 + (13.397 * poids_imc) + (4.799 * taille_imc) - (5.677 * age_imc)
        else:
            bmr = 447.593 + (9.247 * poids_imc) + (3.098 * taille_imc) - (4.330 * age_imc)
        tdee = round(bmr * facteurs[activite_imc])

        if objectif == "Perte de poids":
            calories_cible = tdee - 500
        elif objectif == "Prise de masse":
            calories_cible = tdee + 300
        else:
            calories_cible = tdee

        poids_ideal_min = round(18.5 * ((taille_imc / 100) ** 2), 1)
        poids_ideal_max = round(24.9 * ((taille_imc / 100) ** 2), 1)

        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("IMC", imc, cat_imc)
        col2.metric("Rapport taille/hanche", rth, risque_rth)
        col3.metric("Metabolisme de base", f"{int(bmr)} kcal")
        col4.metric("Calories journalieres", f"{calories_cible} kcal")

        st.markdown(f"**Poids ideal recommande :** entre {poids_ideal_min} kg et {poids_ideal_max} kg")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=imc,
            title={"text": "IMC"},
            gauge={
                "axis": {"range": [10, 45]},
                "bar": {"color": couleur},
                "steps": [
                    {"range": [10, 18.5], "color": "#FFA500"},
                    {"range": [18.5, 25], "color": "#00C851"},
                    {"range": [25, 30], "color": "#FFA500"},
                    {"range": [30, 45], "color": "#FF4500"},
                ],
                "threshold": {"line": {"color": "white", "width": 4}, "value": imc}
            }
        ))
        fig.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# SCORE DE RISQUE CARDIOVASCULAIRE
# ============================================================
with tabs[1]:
    st.markdown("### Score de risque cardiovasculaire sur 10 ans")
    st.markdown("Calcul base sur le score de Framingham")

    col1, col2 = st.columns(2)
    with col1:
        age_cv = st.number_input("Age", 30, 79, 50, key="age_cv")
        sexe_cv = st.selectbox("Sexe", ["Homme", "Femme"], key="sexe_cv")
        tension_cv = st.number_input("Tension systolique (mmHg)", 90, 200, 130, key="t_cv")
        traitement_tension = st.selectbox("Traitement antihypertenseur", ["Non", "Oui"])
    with col2:
        cholesterol_cv = st.number_input("Cholesterol total (mg/dL)", 100, 400, 200)
        hdl_cv = st.number_input("HDL cholesterol (mg/dL)", 20, 100, 50)
        fumeur_cv = st.selectbox("Fumeur actuel", ["Non", "Oui"], key="fum_cv")
        diabete_cv = st.selectbox("Diabete", ["Non", "Oui"], key="diab_cv")

    if st.button("Calculer le risque cardiovasculaire", type="primary"):
        score = 0
        if age_cv < 35: score += 0
        elif age_cv < 40: score += 2
        elif age_cv < 45: score += 5
        elif age_cv < 50: score += 6
        elif age_cv < 55: score += 8
        elif age_cv < 60: score += 10
        elif age_cv < 65: score += 11
        elif age_cv < 70: score += 12
        else: score += 14

        if cholesterol_cv < 160: score += 0
        elif cholesterol_cv < 200: score += 4
        elif cholesterol_cv < 240: score += 7
        elif cholesterol_cv < 280: score += 9
        else: score += 11

        if hdl_cv >= 60: score -= 1
        elif hdl_cv >= 50: score += 0
        elif hdl_cv >= 45: score += 1
        elif hdl_cv >= 35: score += 2
        else: score += 5

        if tension_cv < 120: score += 0
        elif tension_cv < 130: score += 1 if traitement_tension == "Non" else 3
        elif tension_cv < 140: score += 2 if traitement_tension == "Non" else 4
        elif tension_cv < 160: score += 3 if traitement_tension == "Non" else 5
        else: score += 4 if traitement_tension == "Non" else 6

        if fumeur_cv == "Oui": score += 4
        if diabete_cv == "Oui": score += 3

        if score <= 9: risque_pct = 1
        elif score <= 11: risque_pct = 2
        elif score <= 12: risque_pct = 3
        elif score <= 13: risque_pct = 4
        elif score <= 14: risque_pct = 6
        elif score <= 15: risque_pct = 8
        elif score <= 16: risque_pct = 10
        elif score <= 17: risque_pct = 12
        elif score <= 18: risque_pct = 16
        elif score <= 19: risque_pct = 20
        elif score <= 20: risque_pct = 25
        else: risque_pct = 30

        if risque_pct < 5:
            niveau = "Faible"
            couleur_r = "#00C851"
        elif risque_pct < 10:
            niveau = "Modere"
            couleur_r = "#FFA500"
        elif risque_pct < 20:
            niveau = "Eleve"
            couleur_r = "#FF4500"
        else:
            niveau = "Tres eleve"
            couleur_r = "#FF0000"

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Score de Framingham", score)
        col2.metric("Risque sur 10 ans", f"{risque_pct}%")
        col3.metric("Niveau de risque", niveau)

        fig_risque = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risque_pct,
            title={"text": "Risque cardiovasculaire (%)"},
            delta={"reference": 10},
            gauge={
                "axis": {"range": [0, 30]},
                "bar": {"color": couleur_r},
                "steps": [
                    {"range": [0, 5], "color": "#00C851"},
                    {"range": [5, 10], "color": "#FFA500"},
                    {"range": [10, 20], "color": "#FF4500"},
                    {"range": [20, 30], "color": "#FF0000"},
                ],
            }
        ))
        fig_risque.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig_risque, use_container_width=True)

        st.markdown("### Recommandations personnalisees")
        if fumeur_cv == "Oui":
            st.warning("Arreter de fumer reduirait significativement votre risque cardiovasculaire.")
        if tension_cv > 140:
            st.warning("Votre tension arterielle est elevee. Consultez un medecin.")
        if cholesterol_cv > 240:
            st.warning("Votre cholesterol est eleve. Un suivi medical est recommande.")
        if diabete_cv == "Oui":
            st.warning("Le diabete augmente le risque cardiovasculaire. Un suivi strict est important.")
        if risque_pct < 10:
            st.success("Votre risque cardiovasculaire est acceptable. Maintenez un mode de vie sain.")
        else:
            st.error("Votre risque est eleve. Une consultation medicale urgente est recommandee.")
