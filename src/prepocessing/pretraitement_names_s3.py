
import os
import pandas as pd
import boto3

# Paramètres S3
BUCKET_NAME = "mlopsdemlbucket21032"
RAW_KEY = "G_21003_21008_21027_21032/G_21003_21008_21027_21032_Raw/names-mr.csv"
PROCESSED_KEY = "G_21003_21008_21027_21032/G_21003_21008_21027_21032_Processed/names_clean.csv"

# Fichiers locaux
os.makedirs("data", exist_ok=True)
LOCAL_RAW = "data/names-mr.csv"
LOCAL_PROCESSED = "data/names_clean.csv"

# Étape 1 : Télécharger les données brutes depuis S3
print("Téléchargement du fichier names-mr.csv depuis S3...")
s3 = boto3.client('s3')
s3.download_file(BUCKET_NAME, RAW_KEY, LOCAL_RAW)
print("Fichier téléchargé avec succès.")

# Étape 2 : Charger les données
print("Chargement des données...")
df_raw = pd.read_csv(LOCAL_RAW)

# Étape 3 : Nettoyage et transformation
print("Nettoyage et prétraitement...")
df = df_raw['NOMPL;SEXE'].str.split(';', expand=True)
df.columns = ['NOMPL', 'SEXE']
df['NOMPL'] = df['NOMPL'].str.strip()
df['SEXE'] = df['SEXE'].str.strip()
df = df.dropna(subset=['NOMPL', 'SEXE'])
df = df.drop_duplicates()

# Étape 4 : Sauvegarder le résultat localement
print("Sauvegarde du fichier prétraité...")
df.to_csv(LOCAL_PROCESSED, index=False)

# Étape 5 : Upload sur S3
print("Envoi du fichier prétraité vers S3...")
s3.upload_file(LOCAL_PROCESSED, BUCKET_NAME, PROCESSED_KEY)
print("Fichier names_clean.csv sauvegardé sur S3 avec succès.")

print("✅ Prétraitement terminé.")


