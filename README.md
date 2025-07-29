<<<<<<< HEAD
##  Rakiea 21008

- Configuration et lancement d’un serveur MLflow Tracking sur une instance AWS EC2
- Intégration avec les Scripts
- Script utilisé : `evaluate.py`
- Téléchargement des données et du modèle depuis AWS S3
- Extraction des prénoms depuis la colonne `NOMPL`
- Prédiction des sexes (`SEXE`) à l'aide du modèle `LogisticRegression`
- Accuracy calculée sur l'ensemble de test
- Logging des résultats d’évaluation dans MLflow 
- Logging de l’évaluation dans MLflow (URI : `http://13.61.196.51:5000`)
-  Résultat atteint : **accuracy ~ 0.94**
=======
# 🧠 Partie de Touba – Gestion de Version & Entraînement du Modèle

## 📁 Structuration du Repository

- Création et initialisation du dépôt GitHub pour le projet
- Mise en place d'une structure claire :
  ```
  MLOps-projet/
  ├── data/
  ├── models/
  ├── src/
  │   └── train.py
  ├── params.yaml
  └── README.md
  ```
- Ajout des dossiers `.gitignore`, `requirements.txt`, et gestion propre des dépendances

## Gestion Git

- Création de branches : 221003-dev , 21008-dev , 21032-dev , 21027-dev

## 🧪 Script d'entraînement (`train.py`)

- Téléchargement des données d'entraînement depuis S3 (`names_clean.csv`)
- Prétraitement automatique : extraction du prénom (`NOMPL → prenom`)
- Vectorisation des prénoms avec `CountVectorizer` (n-grammes)
- Entraînement d’un modèle `LogisticRegression` avec Scikit-learn
- Calcul et affichage de l'accuracy
- Sauvegarde du modèle localement (`models/`)

## Intégration S3

- Téléchargement des données depuis :
  ```
  s3://mlopsdemlbucket21032/G_.../names_clean.csv
  ```
- Upload automatique du modèle entraîné vers :
  ```
  s3://mlopsdemlbucket21032/G_.../name_gender_model.pkl
  ```

## 📊 Intégration de MLflow

- Suivi complet de l'expérience :
  - Enregistrement des hyperparamètres (`max_iter`, etc.)
  - Logging des métriques (`accuracy`)
  - Logging du modèle entraîné (pickle)
- Lien vers l’interface MLflow :(http://13.61.196.51:5000)

## ✅ Résultat

- Accuracy atteinte : `0.9469` ✅
- Modèle versionné dans MLflow et sur S3
- Code entièrement reproductible à partir du fichier `params.yaml`
>>>>>>> 21003-dev
