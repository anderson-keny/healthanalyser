import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import os

# ============================================================
# CHARGEMENT DES DONNEES
# ============================================================
st.markdown("## Clustering et Reduction de dimensionnalite (PCA)")
st.markdown("---")

if not os.path.exists("data/health_data.csv"):
    st.warning("Aucune donnee disponible. Allez dans Collecte de donnees d abord.")
    st.stop()

df = pd.read_csv("data/health_data.csv")
cols_numeriques = ["age", "poids", "taille", "imc", "tension_systolique",
                   "tension_diastolique", "glycemie", "cholesterol", "frequence_cardiaque"]
cols_disponibles = [c for c in cols_numeriques if c in df.columns]

tabs = st.tabs(["K-Means Clustering", "Clustering Hierarchique", "ACP / PCA"])

# ============================================================
# K-MEANS
# ============================================================
with tabs[0]:
    st.markdown("### K-Means Clustering")
    st.markdown("Regrouper les patients en clusters selon leurs caracteristiques de sante.")

    features_km = st.multiselect(
        "Variables pour le clustering",
        cols_disponibles,
        default=cols_disponibles,
        key="km_features"
    )

    col1, col2 = st.columns(2)
    with col1:
        k = st.slider("Nombre de clusters (K)", 2, 10, 3)
    with col2:
        methode_init = st.selectbox("Methode d initialisation", ["k-means++", "random"])

    if len(features_km) >= 2 and st.button("Lancer K-Means", type="primary"):
        data_km = df[features_km].dropna()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(data_km)

        # ============================================================
        # METHODE DU COUDE
        # ============================================================
        st.markdown("---")
        st.markdown("### Methode du coude")
        inertias = []
        silhouettes = []
        K_range = range(2, 11)
        for ki in K_range:
            km_temp = KMeans(n_clusters=ki, init=methode_init, random_state=42, n_init=10)
            km_temp.fit(X_scaled)
            inertias.append(km_temp.inertia_)
            silhouettes.append(silhouette_score(X_scaled, km_temp.labels_))

        col1, col2 = st.columns(2)
        with col1:
            fig_coude = px.line(
                x=list(K_range), y=inertias,
                markers=True,
                title="Methode du coude (Inertie)",
                labels={"x": "Nombre de clusters", "y": "Inertie"},
                color_discrete_sequence=["#667eea"],
                template="plotly_dark"
            )
            st.plotly_chart(fig_coude, use_container_width=True)

        with col2:
            fig_sil = px.line(
                x=list(K_range), y=silhouettes,
                markers=True,
                title="Score de silhouette",
                labels={"x": "Nombre de clusters", "y": "Silhouette"},
                color_discrete_sequence=["#764ba2"],
                template="plotly_dark"
            )
            st.plotly_chart(fig_sil, use_container_width=True)

        # ============================================================
        # CLUSTERING FINAL
        # ============================================================
        kmeans = KMeans(n_clusters=k, init=methode_init, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        data_km = data_km.copy()
        data_km["Cluster"] = labels.astype(str)

        sil_score = silhouette_score(X_scaled, labels)
        col1, col2, col3 = st.columns(3)
        col1.metric("Nombre de clusters", k)
        col2.metric("Score de silhouette", f"{sil_score:.4f}")
        col3.metric("Inertie finale", f"{kmeans.inertia_:.2f}")

        st.markdown("---")
        pca_viz = PCA(n_components=2)
        X_pca = pca_viz.fit_transform(X_scaled)
        df_viz = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
        df_viz["Cluster"] = labels.astype(str)

        fig_clusters = px.scatter(
            df_viz, x="PC1", y="PC2", color="Cluster",
            title=f"Visualisation des {k} clusters (projection PCA)",
            color_discrete_sequence=["#667eea", "#764ba2", "#f5576c",
                                     "#f093fb", "#4facfe", "#43e97b"],
            template="plotly_dark"
        )
        st.plotly_chart(fig_clusters, use_container_width=True)

        st.markdown("---")
        st.markdown("### Profil moyen par cluster")
        profil = data_km.groupby("Cluster")[features_km].mean().round(2)
        st.dataframe(profil, use_container_width=True)

# ============================================================
# CLUSTERING HIERARCHIQUE
# ============================================================
with tabs[1]:
    st.markdown("### Clustering Hierarchique")

    features_hc = st.multiselect(
        "Variables pour le clustering hierarchique",
        cols_disponibles,
        default=cols_disponibles[:4],
        key="hc_features"
    )

    col1, col2 = st.columns(2)
    with col1:
        n_clusters_hc = st.slider("Nombre de clusters", 2, 8, 3, key="hc_k")
    with col2:
        linkage = st.selectbox("Methode de liaison", ["ward", "complete", "average", "single"])

    if len(features_hc) >= 2 and st.button("Lancer le clustering hierarchique", type="primary"):
        data_hc = df[features_hc].dropna()
        scaler_hc = StandardScaler()
        X_hc = scaler_hc.fit_transform(data_hc)

        hc = AgglomerativeClustering(n_clusters=n_clusters_hc, linkage=linkage)
        labels_hc = hc.fit_predict(X_hc)

        pca_hc = PCA(n_components=2)
        X_pca_hc = pca_hc.fit_transform(X_hc)
        df_hc_viz = pd.DataFrame(X_pca_hc, columns=["PC1", "PC2"])
        df_hc_viz["Cluster"] = labels_hc.astype(str)

        sil_hc = silhouette_score(X_hc, labels_hc)
        col1, col2 = st.columns(2)
        col1.metric("Score de silhouette", f"{sil_hc:.4f}")
        col2.metric("Methode de liaison", linkage)

        fig_hc = px.scatter(
            df_hc_viz, x="PC1", y="PC2", color="Cluster",
            title=f"Clustering hierarchique ({n_clusters_hc} clusters)",
            color_discrete_sequence=["#667eea", "#764ba2", "#f5576c",
                                     "#f093fb", "#4facfe", "#43e97b"],
            template="plotly_dark"
        )
        st.plotly_chart(fig_hc, use_container_width=True)

        data_hc = data_hc.copy()
        data_hc["Cluster"] = labels_hc.astype(str)
        profil_hc = data_hc.groupby("Cluster")[features_hc].mean().round(2)
        st.markdown("### Profil moyen par cluster")
        st.dataframe(profil_hc, use_container_width=True)

# ============================================================
# ACP / PCA
# ============================================================
with tabs[2]:
    st.markdown("### Analyse en Composantes Principales (ACP)")
    st.markdown("Reduire la dimensionnalite des donnees de sante tout en conservant l information.")

    features_pca = st.multiselect(
        "Variables pour la PCA",
        cols_disponibles,
        default=cols_disponibles,
        key="pca_features"
    )

    n_components = st.slider("Nombre de composantes", 2, min(len(features_pca), 9), 3)

    if len(features_pca) >= 2 and st.button("Lancer la PCA", type="primary"):
        data_pca = df[features_pca].dropna()
        scaler_pca = StandardScaler()
        X_pca_scaled = scaler_pca.fit_transform(data_pca)

        pca = PCA(n_components=n_components)
        X_pca_result = pca.fit_transform(X_pca_scaled)

        variance_expliquee = pca.explained_variance_ratio_
        variance_cumulee = np.cumsum(variance_expliquee)

        col1, col2, col3 = st.columns(3)
        col1.metric("Variance expliquee PC1", f"{variance_expliquee[0]*100:.2f}%")
        col2.metric("Variance expliquee PC2", f"{variance_expliquee[1]*100:.2f}%")
        col3.metric("Variance cumulee totale", f"{variance_cumulee[-1]*100:.2f}%")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            fig_var = px.bar(
                x=[f"PC{i+1}" for i in range(n_components)],
                y=variance_expliquee * 100,
                title="Variance expliquee par composante (%)",
                labels={"x": "Composante", "y": "Variance (%)"},
                color=variance_expliquee * 100,
                color_continuous_scale="Blues",
                template="plotly_dark"
            )
            st.plotly_chart(fig_var, use_container_width=True)

        with col2:
            fig_cum = px.line(
                x=[f"PC{i+1}" for i in range(n_components)],
                y=variance_cumulee * 100,
                markers=True,
                title="Variance cumulee (%)",
                labels={"x": "Composante", "y": "Variance cumulee (%)"},
                color_discrete_sequence=["#667eea"],
                template="plotly_dark"
            )
            fig_cum.add_hline(y=95, line_dash="dash",
                line_color="#f5576c", annotation_text="Seuil 95%")
            st.plotly_chart(fig_cum, use_container_width=True)

        st.markdown("---")
        st.markdown("### Projection des patients sur PC1 et PC2")
        df_pca_result = pd.DataFrame(
            X_pca_result[:, :2], columns=["PC1", "PC2"])

        if "niveau_risque" in df.columns:
            df_pca_result["Risque"] = df["niveau_risque"].values[:len(df_pca_result)]
            color_col = "Risque"
        else:
            color_col = None

        fig_proj = px.scatter(
            df_pca_result, x="PC1", y="PC2",
            color=color_col,
            title="Projection ACP des patients (PC1 vs PC2)",
            color_discrete_sequence=["#667eea", "#f5a623", "#f5576c"],
            template="plotly_dark"
        )
        st.plotly_chart(fig_proj, use_container_width=True)

        st.markdown("---")
        st.markdown("### Contribution des variables aux composantes")
        loadings = pd.DataFrame(
            pca.components_.T,
            columns=[f"PC{i+1}" for i in range(n_components)],
            index=features_pca
        ).round(4)
        st.dataframe(loadings, use_container_width=True)

        fig_load = px.imshow(
            loadings,
            text_auto=True,
            title="Carte des contributions (Loadings)",
            color_continuous_scale="RdBu_r",
            template="plotly_dark"
        )
        st.plotly_chart(fig_load, use_container_width=True)
