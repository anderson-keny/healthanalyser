import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import os

# ============================================================
# CHARGEMENT DES DONNEES
# ============================================================
st.markdown("## Regression lineaire")
st.markdown("---")

if not os.path.exists("data/health_data.csv"):
    st.warning("Aucune donnee disponible. Allez dans Collecte de donnees d abord.")
    st.stop()

df = pd.read_csv("data/health_data.csv")
cols_numeriques = ["age", "poids", "taille", "imc", "tension_systolique",
                   "tension_diastolique", "glycemie", "cholesterol", "frequence_cardiaque"]
cols_disponibles = [c for c in cols_numeriques if c in df.columns]

tabs = st.tabs(["Regression simple", "Regression multiple"])

# ============================================================
# REGRESSION LINEAIRE SIMPLE
# ============================================================
with tabs[0]:
    st.markdown("### Regression lineaire simple")
    st.markdown("Modeliser la relation entre deux variables de sante.")

    col1, col2 = st.columns(2)
    with col1:
        var_x = st.selectbox("Variable independante (X)", cols_disponibles, index=0)
    with col2:
        var_y = st.selectbox("Variable dependante (Y)", cols_disponibles, index=3)

    if st.button("Lancer la regression simple", type="primary"):
        data = df[[var_x, var_y]].dropna()
        X = data[[var_x]].values
        y = data[var_y].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("R² Score", f"{r2:.4f}")
        col2.metric("MSE", f"{mse:.4f}")
        col3.metric("MAE", f"{mae:.4f}")
        col4.metric("RMSE", f"{rmse:.4f}")

        st.markdown("---")
        st.markdown("### Equation du modele")
        st.info(f"**{var_y} = {model.coef_[0]:.4f} x {var_x} + {model.intercept_:.4f}**")

        col1, col2 = st.columns(2)
        with col1:
            x_line = np.linspace(X.min(), X.max(), 100)
            y_line = model.coef_[0] * x_line + model.intercept_
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data[var_x], y=data[var_y],
                mode="markers", name="Donnees reelles",
                marker=dict(color="#667eea", opacity=0.6)))
            fig.add_trace(go.Scatter(x=x_line, y=y_line,
                mode="lines", name="Droite de regression",
                line=dict(color="#f5576c", width=3)))
            fig.update_layout(title=f"Regression : {var_x} vs {var_y}",
                template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig_res = go.Figure()
            residuals = y_test - y_pred
            fig_res.add_trace(go.Scatter(x=y_pred, y=residuals,
                mode="markers", marker=dict(color="#764ba2", opacity=0.7),
                name="Residus"))
            fig_res.add_hline(y=0, line_dash="dash", line_color="white")
            fig_res.update_layout(title="Analyse des residus",
                xaxis_title="Valeurs predites", yaxis_title="Residus",
                template="plotly_dark")
            st.plotly_chart(fig_res, use_container_width=True)

        st.markdown("---")
        st.markdown("### Prediction personnalisee")
        val_input = st.number_input(f"Entrer une valeur pour {var_x}", value=float(data[var_x].mean()))
        prediction = model.coef_[0] * val_input + model.intercept_
        st.success(f"Valeur predite pour {var_y} : **{prediction:.4f}**")

# ============================================================
# REGRESSION LINEAIRE MULTIPLE
# ============================================================
with tabs[1]:
    st.markdown("### Regression lineaire multiple")
    st.markdown("Predire une variable a partir de plusieurs variables explicatives.")

    var_cible = st.selectbox("Variable cible (Y)", cols_disponibles, index=3)
    vars_explicatives = st.multiselect(
        "Variables explicatives (X)",
        [c for c in cols_disponibles if c != var_cible],
        default=[c for c in cols_disponibles if c != var_cible][:3]
    )

    if len(vars_explicatives) >= 2 and st.button("Lancer la regression multiple", type="primary"):
        data = df[vars_explicatives + [var_cible]].dropna()
        X = data[vars_explicatives].values
        y = data[var_cible].values

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("R² Score", f"{r2:.4f}")
        col2.metric("MSE", f"{mse:.4f}")
        col3.metric("MAE", f"{mae:.4f}")
        col4.metric("RMSE", f"{rmse:.4f}")

        st.markdown("---")
        st.markdown("### Importance des variables")
        coef_df = pd.DataFrame({
            "Variable": vars_explicatives,
            "Coefficient": model.coef_
        }).sort_values("Coefficient", ascending=True)

        fig_coef = px.bar(
            coef_df, x="Coefficient", y="Variable",
            orientation="h",
            title="Coefficients de regression (variables standardisees)",
            color="Coefficient",
            color_continuous_scale="RdBu",
            template="plotly_dark"
        )
        st.plotly_chart(fig_coef, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig_pred = px.scatter(
                x=y_test, y=y_pred,
                labels={"x": "Valeurs reelles", "y": "Valeurs predites"},
                title="Valeurs reelles vs predites",
                color_discrete_sequence=["#667eea"],
                template="plotly_dark"
            )
            fig_pred.add_shape(type="line",
                x0=y_test.min(), y0=y_test.min(),
                x1=y_test.max(), y1=y_test.max(),
                line=dict(color="white", dash="dash"))
            st.plotly_chart(fig_pred, use_container_width=True)

        with col2:
            residuals = y_test - y_pred
            fig_hist = px.histogram(
                x=residuals, nbins=30,
                title="Distribution des residus",
                color_discrete_sequence=["#764ba2"],
                template="plotly_dark"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
