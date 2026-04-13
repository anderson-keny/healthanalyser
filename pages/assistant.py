import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
import json

# ============================================================
# CONFIGURATION
# ============================================================
st.markdown("## Assistant IA medical")
st.markdown("---")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def appeler_ia(messages, system_prompt):
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": messages
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload
    )
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        return f"Erreur API : {response.status_code} - {response.text}"

system_prompt = """Tu es un assistant medical intelligent specialise dans l analyse
de donnees de sante. Tu analyses les donnees des patients (IMC, tension arterielle,
glycemie, cholesterol, frequence cardiaque, etc.) et fournis des interpretations
claires et des recommandations de sante. Tu preciseras toujours que tes analyses
sont indicatives et ne remplacent pas un avis medical professionnel.
Reponds toujours en francais de maniere claire, structuree et professionnelle."""

tabs = st.tabs(["Analyse d un patient", "Analyse de la base", "Chat medical"])

# ============================================================
# ONGLET 1 : ANALYSE D UN PATIENT
# ============================================================
with tabs[0]:
    st.markdown("### Analyse IA d un profil patient")

    if not ANTHROPIC_API_KEY:
        st.warning("Entrez votre cle API Anthropic pour utiliser l assistant.")
        ANTHROPIC_API_KEY = st.text_input("Cle API Anthropic", type="password")

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", 1, 120, 45, key="ia_age")
        sexe = st.selectbox("Sexe", ["Homme", "Femme"], key="ia_sexe")
        poids = st.number_input("Poids (kg)", 30.0, 250.0, 75.0, key="ia_poids")
        taille = st.number_input("Taille (cm)", 100.0, 220.0, 170.0, key="ia_taille")
    with col2:
        tension_sys = st.number_input("Tension systolique", 60, 250, 130, key="ia_tsys")
        tension_dia = st.number_input("Tension diastolique", 40, 150, 85, key="ia_tdia")
        glycemie = st.number_input("Glycemie (g/L)", 0.5, 5.0, 1.1, key="ia_gly")
        cholesterol = st.number_input("Cholesterol (g/L)", 0.5, 5.0, 2.1, key="ia_chol")
    with col3:
        fc = st.number_input("Frequence cardiaque (bpm)", 30, 200, 78, key="ia_fc")
        fumeur = st.selectbox("Fumeur", ["Non", "Oui"], key="ia_fum")
        diabete = st.selectbox("Diabete", ["Non", "Oui"], key="ia_diab")
        activite = st.selectbox("Activite physique", ["Sedentaire", "Moderee", "Intense"], key="ia_act")

    if st.button("Analyser ce patient avec l IA", type="primary"):
        imc = round(poids / ((taille / 100) ** 2), 2)
        profil = f"""
        Patient : {age} ans, {sexe}
        IMC : {imc} (Poids {poids}kg, Taille {taille}cm)
        Tension arterielle : {tension_sys}/{tension_dia} mmHg
        Glycemie : {glycemie} g/L
        Cholesterol : {cholesterol} g/L
        Frequence cardiaque : {fc} bpm
        Fumeur : {fumeur}
        Diabete : {diabete}
        Activite physique : {activite}
        """
        messages = [{
            "role": "user",
            "content": f"Analyse ce profil de sante et donne une interpretation detaillee avec des recommandations :\n{profil}"
        }]
        with st.spinner("Analyse en cours..."):
            reponse = appeler_ia(messages, system_prompt)
        st.markdown("### Analyse de l IA")
        st.markdown(reponse)

# ============================================================
# ONGLET 2 : ANALYSE DE LA BASE
# ============================================================
with tabs[1]:
    st.markdown("### Analyse globale de la base de donnees")

    if not os.path.exists("data/health_data.csv"):
        st.warning("Aucune donnee disponible. Allez dans Collecte de donnees d abord.")
    else:
        df = pd.read_csv("data/health_data.csv")
        cols_num = ["age", "imc", "tension_systolique", "glycemie", "cholesterol"]
        cols_ok = [c for c in cols_num if c in df.columns]

        stats = df[cols_ok].describe().round(2)
        st.dataframe(stats, use_container_width=True)

        if st.button("Generer un rapport IA de la base", type="primary"):
            resume = f"""
            Base de donnees : {len(df)} patients
            Age moyen : {df['age'].mean():.1f} ans
            IMC moyen : {df['imc'].mean():.2f}
            Tension systolique moyenne : {df['tension_systolique'].mean():.1f} mmHg
            Glycemie moyenne : {df['glycemie'].mean():.2f} g/L
            Cholesterol moyen : {df['cholesterol'].mean():.2f} g/L
            """
            if "niveau_risque" in df.columns:
                resume += f"\nRepartition des risques :\n{df['niveau_risque'].value_counts().to_string()}"
            if "sexe" in df.columns:
                resume += f"\nRepartition par sexe :\n{df['sexe'].value_counts().to_string()}"

            messages = [{
                "role": "user",
                "content": f"Analyse cette base de donnees de sante et redige un rapport medical complet :\n{resume}"
            }]
            with st.spinner("Generation du rapport en cours..."):
                rapport = appeler_ia(messages, system_prompt)
            st.markdown("### Rapport IA")
            st.markdown(rapport)

# ============================================================
# ONGLET 3 : CHAT MEDICAL
# ============================================================
with tabs[2]:
    st.markdown("### Chat avec l assistant medical")

    if "messages_chat" not in st.session_state:
        st.session_state.messages_chat = []

    for msg in st.session_state.messages_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Posez une question medicale...")

    if question:
        st.session_state.messages_chat.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        historique = [{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages_chat]

        with st.chat_message("assistant"):
            with st.spinner("Reflexion en cours..."):
                reponse = appeler_ia(historique, system_prompt)
            st.markdown(reponse)

        st.session_state.messages_chat.append({"role": "assistant", "content": reponse})

    if st.button("Effacer la conversation"):
        st.session_state.messages_chat = []
        st.rerun()
