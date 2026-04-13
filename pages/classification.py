import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                              accuracy_score, roc_curve, auc)
import os

# ============================================================
# CHARGEMENT DES DONNEES
# ============================================================
st.markdown("## Classification supervisee")
st.markdown("---")

if not os.path.exists("data/health_data.csv"):
    st.warning("Aucune donnee disponible. Allez dans Collecte de donnees d abord.")
    st.stop()

df = pd.read_csv("data/health_data.csv")

cols_numeriques = ["age", "poids", "taille", "imc", "tension_systolique",
                   "tension_diastolique", "glycemie", "cholesterol", "frequence_cardiaque"]
cols_disponibles = [c for c in cols_numeriques if c in df.columns]

# ============================================================
# PREPARATION DE LA CIBLE
# ============================================================
st.markdown("### Configuration du modele")

col1, col2 = st.columns(2)
with col1:
    cible = st.selectbox("Variable cible a predire", 
        ["niveau_risque", "diabete", "antecedents_cardiaques", "fumeur"])
with col2:
    algo = st.selectbox("Algorithme de classification", [
        "Random Forest",
        "Regression Logistique",
        "K-Nearest Neighbors",
        "SVM",
        "Gradient Boosting"
    ])

features = st.multiselect(
    "Variables explicatives",
    cols_disponibles,
    default=cols_disponibles
)

if len(features) < 2:
    st.warning("Selectionnez au moins 2 variables explicatives.")
    st.stop()

if st.button("Lancer la classification", type="primary"):

    data = df[features + [cible]].dropna()
    X = data[features]
    y = data[cible]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    # ============================================================
    # SELECTION DU MODELE
    # ============================================================
    if algo == "Random Forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif algo == "Regression Logistique":
        model = LogisticRegression(max_iter=1000, random_state=42)
    elif algo == "K-Nearest Neighbors":
        model = KNeighborsClassifier(n_neighbors=5)
    elif algo == "SVM":
        model = SVC(probability=True, random_state=42)
    else:
        model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None

    accuracy = accuracy_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X_scaled, y_encoded, cv=5)

    # ============================================================
    # METRIQUES
    # ============================================================
    st.markdown("---")
    st.markdown("### Resultats du modele")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precision globale", f"{accuracy*100:.2f}%")
    col2.metric("CV Score moyen", f"{cv_scores.mean()*100:.2f}%")
    col3.metric("CV Ecart-type", f"{cv_scores.std()*100:.2f}%")
    col4.metric("Taille test", f"{len(y_test)} patients")

    # ============================================================
    # MATRICE DE CONFUSION
    # ============================================================
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Matrice de confusion")
        cm = confusion_matrix(y_test, y_pred)
        labels = le.classes_
        fig_cm = px.imshow(
            cm, text_auto=True,
            x=labels, y=labels,
            title="Matrice de confusion",
            color_continuous_scale="Blues",
            template="plotly_dark"
        )
        st.plotly_chart(fig_cm, use_container_width=True)

    with col2:
        st.markdown("### Importance des variables")
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        elif hasattr(model, "coef_"):
            importances = np.abs(model.coef_[0])
        else:
            importances = np.ones(len(features))

        feat_df = pd.DataFrame({
            "Variable": features,
            "Importance": importances
        }).sort_values("Importance", ascending=True)

        fig_imp = px.bar(
            feat_df, x="Importance", y="Variable",
            orientation="h",
            title="Importance des variables",
            color="Importance",
            color_continuous_scale="Viridis",
            template="plotly_dark"
        )
        st.plotly_chart(fig_imp, use_container_width=True)

    # ============================================================
    # COURBE ROC
    # ============================================================
    if y_proba is not None and len(le.classes_) == 2:
        st.markdown("---")
        st.markdown("### Courbe ROC")
        fpr, tpr, _ = roc_curve(y_test, y_proba[:, 1])
        roc_auc = auc(fpr, tpr)
        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines",
            name=f"ROC (AUC = {roc_auc:.3f})",
            line=dict(color="#667eea", width=3)))
        fig_roc.add_shape(type="line", x0=0, y0=0, x1=1, y1=1,
            line=dict(color="white", dash="dash"))
        fig_roc.update_layout(
            title="Courbe ROC",
            xaxis_title="Taux de faux positifs",
            yaxis_title="Taux de vrais positifs",
            template="plotly_dark"
        )
        st.plotly_chart(fig_roc, use_container_width=True)

    # ============================================================
    # RAPPORT DE CLASSIFICATION
    # ============================================================
    st.markdown("---")
    st.markdown("### Rapport de classification detaille")
    report = classification_report(y_test, y_pred,
        target_names=le.classes_, output_dict=True)
    report_df = pd.DataFrame(report).transpose().round(3)
    st.dataframe(report_df, use_container_width=True)

    # ============================================================
    # PREDICTION MANUELLE
    # ============================================================
    st.markdown("---")
    st.markdown("### Prediction pour un nouveau patient")
    input_vals = {}
    cols = st.columns(len(features))
    for i, feat in enumerate(features):
        with cols[i]:
            input_vals[feat] = st.number_input(
                feat, value=float(df[feat].mean()))

    if st.button("Predire le risque", type="primary"):
        input_df = pd.DataFrame([input_vals])
        input_scaled = scaler.transform(input_df)
        pred = model.predict(input_scaled)
        pred_label = le.inverse_transform(pred)[0]
        proba = model.predict_proba(input_scaled)[0] if hasattr(model, "predict_proba") else None

        st.success(f"Prediction : **{pred_label}**")
        if proba is not None:
            proba_df = pd.DataFrame({
                "Classe": le.classes_,
                "Probabilite": proba
            })
            fig_proba = px.bar(
                proba_df, x="Classe", y="Probabilite",
                title="Probabilites par classe",
                color="Probabilite",
                color_continuous_scale="Blues",
                template="plotly_dark"
            )
            st.plotly_chart(fig_proba, use_container_width=True)
