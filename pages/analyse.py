import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ============================================================
# CHARGEMENT DES DONNEES
# ============================================================
st.markdown("## Analyse descriptive des donnees de sante")
st.markdown("---")

if not os.path.exists("data/health_data.csv"):
    st.warning("Aucune donnee disponible. Allez dans Collecte de donnees d abord.")
    st.stop()

df = pd.read_csv("data/health_data.csv")
st.success(f"Base de donnees chargee : {len(df)} patients, {len(df.columns)} variables")

# ============================================================
# STATISTIQUES GENERALES
# ============================================================
st.markdown("### Statistiques generales")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Nombre de patients", len(df))
col2.metric("Age moyen", f"{df['age'].mean():.1f} ans")
col3.metric("IMC moyen", f"{df['imc'].mean():.1f}")
col4.metric("Tension moyenne", f"{df['tension_systolique'].mean():.0f} mmHg")

st.markdown("---")
st.markdown("### Tableau des statistiques descriptives")
cols_numeriques = ["age", "poids", "taille", "imc", "tension_systolique",
                   "tension_diastolique", "glycemie", "cholesterol", "frequence_cardiaque"]
cols_disponibles = [c for c in cols_numeriques if c in df.columns]
st.dataframe(df[cols_disponibles].describe().round(2), use_container_width=True)

# ============================================================
# DISTRIBUTIONS
# ============================================================
st.markdown("---")
st.markdown("### Distribution des variables numeriques")
variable = st.selectbox("Choisir une variable", cols_disponibles)

col1, col2 = st.columns(2)
with col1:
    fig_hist = px.histogram(
        df, x=variable, nbins=30,
        title=f"Distribution de {variable}",
        color_discrete_sequence=["#667eea"],
        template="plotly_dark"
    )
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(
        df, y=variable, x="sexe" if "sexe" in df.columns else None,
        title=f"Boite a moustaches : {variable}",
        color="sexe" if "sexe" in df.columns else None,
        color_discrete_sequence=["#667eea", "#764ba2"],
        template="plotly_dark"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ============================================================
# ANALYSE DE L IMC
# ============================================================
st.markdown("---")
st.markdown("### Analyse de l IMC")

if "statut_imc" not in df.columns:
    df["statut_imc"] = pd.cut(df["imc"],
        bins=[0, 18.5, 25, 30, 100],
        labels=["Sous-poids", "Normal", "Surpoids", "Obesite"])

col1, col2 = st.columns(2)
with col1:
    imc_counts = df["statut_imc"].value_counts()
    fig_imc = px.pie(
        values=imc_counts.values,
        names=imc_counts.index,
        title="Repartition des statuts IMC",
        color_discrete_sequence=["#667eea", "#764ba2", "#f093fb", "#f5576c"],
        template="plotly_dark"
    )
    st.plotly_chart(fig_imc, use_container_width=True)

with col2:
    fig_imc_age = px.scatter(
        df, x="age", y="imc",
        color="statut_imc" if "statut_imc" in df.columns else None,
        title="IMC en fonction de l age",
        color_discrete_sequence=["#667eea", "#764ba2", "#f093fb", "#f5576c"],
        template="plotly_dark"
    )
    st.plotly_chart(fig_imc_age, use_container_width=True)

# ============================================================
# CORRELATIONS
# ============================================================
st.markdown("---")
st.markdown("### Matrice de correlation")

corr = df[cols_disponibles].corr().round(2)
fig_corr = px.imshow(
    corr,
    text_auto=True,
    title="Correlation entre les variables de sante",
    color_continuous_scale="RdBu_r",
    template="plotly_dark"
)
fig_corr.update_layout(height=500)
st.plotly_chart(fig_corr, use_container_width=True)

# ============================================================
# ANALYSE PAR GROUPE
# ============================================================
st.markdown("---")
st.markdown("### Analyse par groupe")

col1, col2 = st.columns(2)
with col1:
    var_x = st.selectbox("Variable X", cols_disponibles, index=0)
with col2:
    var_y = st.selectbox("Variable Y", cols_disponibles, index=2)

couleur = st.selectbox("Colorer par", ["sexe", "fumeur", "diabete", "antecedents_cardiaques", "activite_physique"])

fig_scatter = px.scatter(
    df, x=var_x, y=var_y,
    color=couleur if couleur in df.columns else None,
    title=f"{var_x} vs {var_y}",
    trendline="ols",
    color_discrete_sequence=["#667eea", "#764ba2", "#f093fb"],
    template="plotly_dark"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================================
# REPARTITION DES RISQUES
# ============================================================
st.markdown("---")
st.markdown("### Repartition des niveaux de risque cardiaque")

if "niveau_risque" in df.columns:
    col1, col2 = st.columns(2)
    with col1:
        risque_counts = df["niveau_risque"].value_counts()
        fig_risque = px.bar(
            x=risque_counts.index,
            y=risque_counts.values,
            title="Niveaux de risque cardiaque",
            color=risque_counts.index,
            color_discrete_map={"Faible": "#667eea", "Modere": "#f5a623", "Eleve": "#f5576c"},
            template="plotly_dark"
        )
        st.plotly_chart(fig_risque, use_container_width=True)

    with col2:
        fig_risque_sexe = px.histogram(
            df, x="niveau_risque", color="sexe",
            barmode="group",
            title="Risque cardiaque par sexe",
            color_discrete_sequence=["#667eea", "#764ba2"],
            template="plotly_dark"
        )
        st.plotly_chart(fig_risque_sexe, use_container_width=True)
else:
    st.info("Colonne niveau_risque non disponible dans ce jeu de donnees.")
