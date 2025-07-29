# Projet MLOps — Prétraitement des Noms

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

## 📁 Notes sur .gitignore

Deux fichiers `.gitignore` sont présents :

- `.dvc/.gitignore` : ignore les caches internes de DVC
- `data/.gitignore` : empêche Git de suivre `names_clean.csv` géré par DVC

---

## ✅ Résultat attendu

- Le fichier nettoyé `names_clean.csv` est suivi proprement par DVC
- Toutes les données sont traçables et stockées de façon reproductible
- Le script Python est prêt à être réutilisé ou intégré dans un pipeline

---

## 📬 Contact
Pour toute question ou revue du code : Oumlvadli — Branche `21032-dev`
