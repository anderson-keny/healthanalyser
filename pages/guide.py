import streamlit as st

st.markdown("## Guide d utilisation complet")
st.markdown("---")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;'>
<h2 style='color:white; text-align:center;'>MCLAURENT HEALTH DIAGNOSTIC CENTER</h2>
<p style='color:#e0e0e0; text-align:center; font-style:italic;'>Guide complet d utilisation - INF232 EC2</p>
<p style='color:#e0e0e0; text-align:center;'>Auteur : ASSOUMOU YENE LAURENT KEVIN JAMES | Matricule : 24G2332</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "Introduction",
    "Collecte de donnees",
    "Analyse descriptive",
    "Regression",
    "Classification",
    "Clustering et PCA",
    "Outils medicaux",
    "Assistant IA"
])

with tabs[0]:
    st.markdown("""
### Qu est-ce que MCLAURENT HEALTH DIAGNOSTIC CENTER ?

Cette application est une **plateforme intelligente d analyse de donnees de sante**. Elle permet a un utilisateur de :
- Collecter des donnees medicales sur des patients
- Analyser ces donnees de facon visuelle et statistique
- Utiliser des algorithmes d intelligence artificielle pour faire des predictions
- Obtenir des recommandations medicales personnalisees

Elle a ete concue dans le cadre du cours **INF232 EC2 - Analyse de donnees** et couvre les 5 techniques suivantes :
1. Regression lineaire simple et multiple
2. Techniques de reduction de dimensionnalite (PCA)
3. Classification supervisee (Random Forest, Regression Logistique, KNN, SVM, Gradient Boosting)
4. Classification non supervisee (K-Means, Clustering Hierarchique)
5. Analyse descriptive complete

---
### Comment naviguer dans l application ?

Sur la **gauche de l ecran**, vous trouverez un menu appele **Menu** avec toutes les sections disponibles. Cliquez sur n importe quelle section pour y acceder.

Les sections disponibles sont :
- **Accueil** : Vue generale de l application
- **Collecte de donnees** : Entrer ou importer des donnees
- **Analyse descriptive** : Voir les statistiques et graphiques
- **Regression** : Predire des valeurs numeriques
- **Classification** : Predire des categories
- **Clustering et PCA** : Regrouper les patients
- **Outils medicaux** : Calculateurs medicaux avances
- **Assistant IA** : Poser des questions a l intelligence artificielle
- **Guide d utilisation** : Ce guide que vous lisez en ce moment
""")

with tabs[1]:
    st.markdown("""
### Collecte de donnees

Cette section permet d **entrer les donnees des patients** dans l application. Il y a 4 facons de le faire :

---
#### Onglet 1 : Saisie manuelle
Vous remplissez vous-meme les informations d un patient :
- **Nom** : le nom du patient
- **Age** : en annees
- **Sexe** : Homme ou Femme
- **Poids** : en kilogrammes
- **Taille** : en centimetres
- **Tension systolique** : la pression maximale du coeur (normale : 120 mmHg)
- **Tension diastolique** : la pression minimale du coeur (normale : 80 mmHg)
- **Glycemie** : taux de sucre dans le sang (normale : entre 0.7 et 1.1 g/L)
- **Cholesterol** : taux de graisses dans le sang (normale : moins de 2.0 g/L)
- **Frequence cardiaque** : nombre de battements par minute (normale : 60-100 bpm)
- **Fumeur** : Oui ou Non
- **Activite physique** : Sedentaire, Moderee ou Intense
- **Diabete** : Oui ou Non
- **Antecedents cardiaques** : Oui ou Non

Apres avoir rempli tous les champs, cliquez sur **Enregistrer le patient**. L application calcule automatiquement :
- L **IMC** (Indice de Masse Corporelle) = poids / (taille en metres)²
- Le **statut IMC** : Sous-poids, Normal, Surpoids, Obesite
- Le **niveau de risque cardiaque** : Faible, Modere ou Eleve

---
#### Onglet 2 : Import CSV/Excel
Si vous avez deja un fichier de donnees sur votre ordinateur :
1. Cliquez sur **Browse files**
2. Selectionnez votre fichier (.csv, .xlsx ou .xls)
3. Verifiez l apercu des donnees affichees
4. Cliquez sur **Sauvegarder ces donnees**

---
#### Onglet 3 : Donnees depuis URL
Si vos donnees sont disponibles sur internet :
1. Copiez le lien direct vers le fichier CSV
2. Collez-le dans le champ URL
3. Cliquez sur **Charger depuis URL**

---
#### Onglet 4 : Generation synthetique
Pour tester l application sans avoir de vraies donnees :
1. Utilisez le **curseur** pour choisir le nombre de patients (entre 50 et 1000)
2. Cliquez sur **Generer les donnees**
3. L application cree automatiquement des patients fictifs avec des valeurs realistes

---
#### Comment interpreter les resultats ?
Apres la saisie, vous verrez :
- **IMC** : Valeur numerique avec sa categorie
- **Niveau de risque** : Faible (score 0-1), Modere (score 2-3), Eleve (score 4+)
- **Score de risque** : calculé sur 7 facteurs de risque
""")

with tabs[2]:
    st.markdown("""
### Analyse descriptive

Cette section montre des **statistiques et graphiques** sur toutes les donnees collectees.

---
#### Statistiques generales
En haut de la page, vous voyez 4 indicateurs cles :
- Nombre total de patients
- Age moyen
- IMC moyen
- Tension arterielle moyenne

---
#### Tableau des statistiques descriptives
Ce tableau montre pour chaque variable numerique :
- **count** : nombre de valeurs
- **mean** : moyenne
- **std** : ecart-type (dispersion des valeurs)
- **min / max** : valeurs minimale et maximale
- **25%, 50%, 75%** : quartiles (25% = la valeur en dessous de laquelle se trouvent 25% des donnees)

---
#### Distribution des variables
Choisissez une variable dans le menu deroulant pour voir :
- **Histogramme** (gauche) : montre combien de patients ont chaque valeur. Les barres hautes indiquent des valeurs frequentes.
- **Boite a moustaches** (droite) : montre la distribution par sexe. La ligne du milieu est la mediane, la boite contient 50% des donnees.

---
#### Analyse de l IMC
- **Graphique en camembert** : proportions des categories IMC dans la population
- **Nuage de points** : relation entre l age et l IMC

---
#### Matrice de correlation
Ce graphique montre comment les variables sont liees entre elles :
- **Rouge fonce** : forte correlation positive (quand l une augmente, l autre aussi)
- **Bleu fonce** : forte correlation negative (quand l une augmente, l autre diminue)
- **Blanc** : pas de correlation

---
#### Analyse par groupe
Choisissez deux variables et une couleur de groupe pour voir les relations entre elles sur un nuage de points avec droite de tendance.

---
#### Repartition des niveaux de risque
Graphiques montrant la distribution des niveaux de risque cardiaque dans la population, par sexe.
""")

with tabs[3]:
    st.markdown("""
### Regression lineaire

La regression permet de **predire une valeur numerique** a partir d autres valeurs.

---
#### Onglet 1 : Regression simple
Predit une variable a partir d **une seule** variable.

**Comment utiliser :**
1. Choisissez la **variable X** (celle qu on connait, ex: age)
2. Choisissez la **variable Y** (celle qu on veut predire, ex: IMC)
3. Cliquez sur **Lancer la regression simple**

**Comment interpreter les resultats :**
- **R² Score** : entre 0 et 1. Plus il est proche de 1, meilleur est le modele. Ex: 0.85 signifie que le modele explique 85% de la variation.
- **MSE** (Mean Squared Error) : erreur moyenne au carre. Plus petit = meilleur.
- **MAE** (Mean Absolute Error) : erreur absolue moyenne en unite de la variable.
- **RMSE** : racine de MSE, dans la meme unite que la variable predite.

**Graphiques :**
- **Droite de regression** : la ligne rouge montre la prediction. Les points bleus sont les donnees reelles.
- **Analyse des residus** : les residus sont les erreurs. Ils doivent etre disperses aleatoirement autour de zero.

**Prediction personnalisee :**
Entrez une valeur pour X et obtenez immediatement la prediction pour Y.

---
#### Onglet 2 : Regression multiple
Predit une variable a partir de **plusieurs** variables.

**Comment utiliser :**
1. Choisissez la **variable cible Y**
2. Selectionnez plusieurs **variables explicatives X**
3. Cliquez sur **Lancer la regression multiple**

**Comment interpreter :**
- **Graphique des coefficients** : les barres montrent l importance et la direction de chaque variable. Une barre positive signifie que cette variable fait augmenter Y, negative qu elle la fait diminuer.
- **Valeurs reelles vs predites** : les points doivent etre proches de la diagonale pour un bon modele.
""")

with tabs[4]:
    st.markdown("""
### Classification supervisee

La classification permet de **predire une categorie** pour un patient.

---
#### Comment utiliser :
1. Choisissez la **variable cible** a predire (ex: niveau_risque = Faible/Modere/Eleve)
2. Choisissez l **algorithme** :
   - **Random Forest** : utilise plusieurs arbres de decision. Tres fiable.
   - **Regression Logistique** : modele statistique simple et interpretable.
   - **K-Nearest Neighbors** : classe selon les voisins les plus proches.
   - **SVM** : trouve la meilleure frontiere entre les classes.
   - **Gradient Boosting** : combine plusieurs modeles faibles pour un resultat fort.
3. Selectionnez les **variables explicatives**
4. Cliquez sur **Lancer la classification**

---
#### Comment interpreter les resultats :

**Precision globale** : pourcentage de bonnes predictions. Ex: 92% signifie que 92 patients sur 100 sont bien classes.

**CV Score** : score de validation croisee. L application teste le modele 5 fois sur differentes parties des donnees pour verifier qu il ne triche pas.

**Matrice de confusion** : tableau qui montre les bonnes et mauvaises predictions.
- Les chiffres sur la diagonale = bonnes predictions
- Les autres chiffres = erreurs

**Importance des variables** : montre quelles variables influencent le plus la prediction. Une barre longue = variable tres importante.

**Courbe ROC** : pour les classifications binaires. Plus la courbe est proche du coin superieur gauche, meilleur est le modele. L **AUC** (aire sous la courbe) doit etre proche de 1.

**Prediction manuelle** : entrez les valeurs d un nouveau patient et obtenez immediatement sa categorie predite avec les probabilites.
""")

with tabs[5]:
    st.markdown("""
### Clustering et PCA

---
#### Onglet 1 : K-Means Clustering
Le clustering permet de **regrouper automatiquement** les patients en groupes similaires sans avoir de categories predefinies.

**Comment utiliser :**
1. Selectionnez les variables a utiliser
2. Choisissez le nombre de clusters K
3. Cliquez sur **Lancer K-Means**

**Comment interpreter :**

**Methode du coude** : ce graphique aide a choisir le bon nombre de clusters. On cherche le point ou la courbe fait un "coude" - c est la le nombre optimal de clusters.

**Score de silhouette** : entre -1 et 1. Plus il est proche de 1, mieux les patients sont regroupes. Au-dessus de 0.5 = bon clustering.

**Visualisation des clusters** : chaque couleur represente un groupe de patients similaires.

**Profil moyen par cluster** : tableau montrant les caracteristiques moyennes de chaque groupe. Cela permet de comprendre ce qui distingue les groupes.

---
#### Onglet 2 : Clustering Hierarchique
Similaire au K-Means mais utilise une methode differente de regroupement.

Les **methodes de liaison** determinent comment les distances entre groupes sont calculees :
- **ward** : minimise la variance dans chaque groupe (recommande)
- **complete** : utilise la distance maximale
- **average** : utilise la distance moyenne

---
#### Onglet 3 : ACP / PCA
L **Analyse en Composantes Principales** reduit le nombre de variables tout en conservant le maximum d information.

**Pourquoi l utiliser ?** Quand vous avez beaucoup de variables (9 ici), il est difficile de les visualiser toutes ensemble. La PCA les compresse en 2 ou 3 dimensions.

**Comment interpreter :**

**Variance expliquee** : chaque composante PC explique un pourcentage de l information totale. PC1 explique le plus, PC2 le deuxieme plus, etc.

**Variance cumulee** : la somme des variances. On recommande d avoir au moins 80-90% de variance expliquee.

**Projection** : chaque point est un patient. Les patients proches ont des caracteristiques similaires.

**Loadings** : contribution de chaque variable originale aux composantes. Une valeur elevee (positive ou negative) signifie que cette variable est importante pour cette composante.
""")

with tabs[6]:
    st.markdown("""
### Outils medicaux avances

---
#### Onglet 1 : Calculateur IMC avance

En plus de l IMC classique, cet outil calcule :

**Rapport taille/hanche (RTH)** : mesure la repartition des graisses.
- Homme : risque eleve si RTH > 0.9
- Femme : risque eleve si RTH > 0.85
- Un RTH eleve indique un risque accru de maladies cardiovasculaires.

**Metabolisme de base (BMR)** : nombre de calories que votre corps brule au repos.

**Depense energetique totale (TDEE)** : calories totales brulees en une journee selon votre niveau d activite.

**Calories cibles** : recommandation calorique selon votre objectif (perte de poids, maintien, prise de masse).

**Jaugeur IMC** : graphique en forme de compteur de vitesse qui montre visuellement ou se situe votre IMC.

---
#### Onglet 2 : Score de risque cardiovasculaire (Framingham)

Ce calculateur estime votre **probabilite d avoir un evenement cardiovasculaire dans les 10 prochaines annees**.

Il utilise le **Score de Framingham**, un outil medical reconnu internationalement.

**Variables utilisees :**
- Age, sexe, tension arterielle
- Cholesterol total et HDL (bon cholesterol)
- Tabagisme, diabete, traitement antihypertenseur

**Interpretation du risque :**
- Moins de 5% : risque **Faible** - continuez vos bonnes habitudes
- 5 a 10% : risque **Modere** - consultez votre medecin pour un suivi
- 10 a 20% : risque **Eleve** - consultation medicale recommandee
- Plus de 20% : risque **Tres eleve** - consultation urgente necessaire

**Recommandations personnalisees** : l application affiche des conseils specifiques selon vos facteurs de risque.
""")

with tabs[7]:
    st.markdown("""
### Assistant IA medical

Cet outil utilise une **intelligence artificielle** pour analyser des donnees de sante et repondre a des questions medicales.

---
#### Onglet 1 : Analyse d un patient
Entrez les informations d un patient et cliquez sur **Analyser ce patient avec l IA**.

L IA va :
- Interpreter chaque indicateur de sante
- Identifier les facteurs de risque
- Donner des recommandations personnalisees
- Expliquer les resultats en langage simple

**Important** : une cle API Anthropic est necessaire. Cette cle permet a l application de communiquer avec l intelligence artificielle.

---
#### Onglet 2 : Analyse de la base
Cliquez sur **Generer un rapport IA de la base** pour obtenir une analyse complete de toute la population de patients enregistres.

---
#### Onglet 3 : Chat medical
Posez n importe quelle question medicale en langage naturel.

Exemples de questions :
- "Qu est-ce que l hypertension arterielle ?"
- "Quels sont les symptomes du diabete ?"
- "Comment reduire mon cholesterol naturellement ?"
- "Mon IMC est de 27, est-ce dangereux ?"

L assistant conserve le contexte de la conversation pour des reponses coherentes.

**Note importante** : l assistant IA fournit des informations generales. Il ne remplace pas une consultation medicale professionnelle.

---
### Avertissement general

Toutes les analyses et predictions de cette application sont basees sur des **donnees statistiques** et des **algorithmes d apprentissage automatique**. Elles sont fournies a titre **informatif et educatif uniquement**. Pour tout probleme de sante, consultez toujours un **professionnel de sante qualifie**.
""")
