import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os

st.set_page_config(
    page_title="HealthAnalytics AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%); }
    .title-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102,126,234,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #1e2130 0%, #2d3250 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## MENU")
    st.markdown("---")
    selected = option_menu(
        menu_title=None,
        options=["Accueil", "Collecte de donnees", "Analyse descriptive", "Regression", "Classification", "Clustering et PCA", "Outils medicaux", "Assistant IA", "Guide d utilisation", "Licence"],
        icons=["house", "database", "bar-chart", "graph-up", "shield-check", "diagram-3", "heart-pulse", "robot", "book", "award"],
        default_index=0,
        styles={
            "container": {"background-color": "#1e2130"},
            "icon": {"color": "#667eea", "font-size": "16px"},
            "nav-link": {"color": "#ffffff", "font-size": "14px"},
            "nav-link-selected": {"background-color": "#667eea"},
        }
    )
    st.markdown("---")
    st.markdown("INF232 EC2")
    st.markdown("Analyse de donnees sante")

if selected == "Accueil":
    st.markdown("""
    <div class='title-card'>
        <h1 style='font-size:2.5rem; background: linear-gradient(90deg, #FFD700, #FF6B6B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; letter-spacing: 2px;'>MCLAURENT HEALTH DIAGNOSTIC CENTER</h1>
        <p style='color:#00E5FF; font-size:1.3rem; font-style: italic; font-weight: 600; letter-spacing: 3px; text-shadow: 0 0 10px #00E5FF;'>" YOUR HEALTH, OUR HAPPINESS "</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Modules", "6", "Complets")
    with col2:
        st.metric("IA integree", "4", "Algorithmes")
    with col3:
        st.metric("Visualisations", "10+", "Graphiques")
    with col4:
        st.metric("Precision", "95%+", "Modeles")

    st.markdown("---")
    st.markdown("### Fonctionnalites principales")
    col1, col2 = st.columns(2)
    with col1:
        st.success("Collecte multi-sources : CSV, Manuel, API, Synthetique")
        st.success("Analyse descriptive complete")
        st.success("Regression lineaire simple et multiple")
    with col2:
        st.success("Classification supervisee : risque cardiaque")
        st.success("Clustering K-Means et PCA")
        st.success("Assistant IA medical integre")

    if os.path.exists("data/health_data.csv"):
        df = pd.read_csv("data/health_data.csv")
        st.markdown("---")
        st.markdown("### Apercu des donnees actuelles")
        st.dataframe(df.tail(5), use_container_width=True)
        st.info(f"{len(df)} patients enregistres dans la base de donnees")
    else:
        st.warning("Aucune donnee encore. Allez dans Collecte de donnees pour commencer.")


    st.markdown("---")
    st.markdown("### A propos de l auteur")
    col_photo, col_info = st.columns([1, 3])
    with col_photo:
        if os.path.exists("assets/photo.jpg"):
            st.image("assets/photo.jpg", width=180)
    with col_info:
        st.markdown("**ASSOUMOU YENE LAURENT KEVIN JAMES**")
        st.markdown("Matricule : **24G2332**")
        st.markdown("Niveau 2 - Universite de Yaounde I")
        st.markdown("Departement Informatique - INF232 EC2")
        st.markdown("Republique du Cameroun")

elif selected == "Collecte de donnees":
    exec(open("pages/collecte.py").read())
elif selected == "Analyse descriptive":
    exec(open("pages/analyse.py").read())
elif selected == "Regression":
    exec(open("pages/regression.py").read())
elif selected == "Classification":
    exec(open("pages/classification.py").read())
elif selected == "Clustering et PCA":
    exec(open("pages/clustering.py").read())
elif selected == "Outils medicaux":
 exec(open("pages/outils.py").read())
elif selected == "Licence":
 exec(open("pages/licence.py").read())
elif selected == "Guide d utilisation":
 exec(open("pages/guide.py").read())
elif selected == "Assistant IA":
    exec(open("pages/assistant.py").read())
