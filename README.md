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
