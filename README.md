<<<<<<< HEAD
## Rakiea 21008

- Configuration et lancement d’un serveur MLflow Tracking sur une instance AWS EC2
- Intégration avec les Scripts
- Script utilisé : `evaluate.py`
- Téléchargement des données et du modèle depuis AWS S3
- Extraction des prénoms depuis la colonne `NOMPL`
- Prédiction des sexes (`SEXE`) à l'aide du modèle `LogisticRegression`
- Accuracy calculée sur l'ensemble de test
- Logging des résultats d’évaluation dans MLflow
- Logging de l’évaluation dans MLflow (URI : `http://13.61.196.51:5000`)
- Résultat atteint : **accuracy ~ 0.94**

# 🧠 Partie de Touba 21003 – Gestion de Version & Entraînement du Modèle

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
=======
# Projet MLOps —

## 👤 Réalisé par
**Oumlvadli** — Branche : `21032-dev`

---

## Objectif du projet

Cette Partie vise à appliquer des outils MLOps pour gérer le cycle de vie des données, notamment avec DVC, AWS S3 et Git.  

- DVC (Data Version Control) pour le suivi des fichiers de données
- Git pour la gestion de code collaboratif
- AWS S3 pour le stockage cloud
- Python pour le prétraitement

---

## Structure du projet

```
mlops_projet/
├── data/                         # Données brutes et nettoyées
│   ├── names-mr.csv              # Données brutes
│   ├── names_clean.csv.dvc       # Données nettoyées (versionnées)
│
├── src/preprocessing/            # Script de prétraitement
│   └── pretraitement_names_s3.py
│
├── .dvc/                         # Config DVC
├── .gitignore                    # Fichiers ignorés par Git
├── .dvcignore                    # Fichiers ignorés par DVC
├── README.md                     # Ce fichier
└── requirements.txt              # Dépendances Python
```

---

## Étapes réalisées

### 1. Prétraitement des données
- Chargement du fichier `names-mr.csv`
- Nettoyage : suppression des doublons et lignes incomplètes
- Export du fichier nettoyé sous `names_clean.csv`

### 2. Versionnement avec DVC
- Seul le fichier `names_clean.csv` est suivi par DVC

### 3. Stockage distant avec S3
- Configuration d’un remote DVC connecté à AWS S3
- Poussée des données versionnées avec `dvc push`

---

## Lancer le prétraitement

Assurez-vous que les dépendances sont installées :

```bash
pip install -r requirements.txt
```

Puis exécutez le script :

```bash
python src/preprocessing/pretraitement_names_s3.py
```

---

## Dépendances

→ Voir fichier [requirements.txt](./requirements.txt)

---

## Notes sur .gitignore

Deux fichiers `.gitignore` sont présents :

- `.dvc/.gitignore` : ignore les caches internes de DVC
- `data/.gitignore` : empêche Git de suivre `names_clean.csv` géré par DVC

---

## Résultat attendu

- Le fichier nettoyé `names_clean.csv` est suivi proprement par DVC
- Toutes les données sont traçables et stockées de façon reproductible
- Le script Python est prêt à être réutilisé ou intégré dans un pipeline

---

## Contact
Pour toute question ou revue du code : Oumlvadli — Branche `21032-dev`

=======
#Realise par 21027
# Projet Flask - Prédiction de Genre

Cette application Flask permet de prédire le genre (homme/femme) à partir d’un prénom.  
Elle utilise un modèle de machine learning entraîné et stocké en local (`name_gender_model.pkl` et `name_gender_vectorizer.pkl`).

---

## 📁 Structure du projet
connect sur EC2(mlflow-EC2-21003)

cd flaskapp

active pipenv shell

cd
 Projet_flask/
│
├── app.py # Application Flask principale
├── templates/ # Fichiers HTML (interface utilisateur)
├── name_gender_model.pkl # Modèle ML entraîné
├── name_gender_vectorizer.pkl # Vectoriseur associé
├── mlruns/ # (optionnel) Logs
Execute python3 app.py

http://127.0.0.1:5000/
http://16.16.212.94:5000/(IPpub<EC2>)
>>>>>>> 21027-dev
