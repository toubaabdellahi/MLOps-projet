# import os
# import yaml
# import boto3
# import joblib
# import pandas as pd
# from urllib.parse import urlparse
# from sklearn.feature_extraction.text import TfidfVectorizer

# def download_from_s3(bucket: str, key: str, local_path: str):
#     """Télécharge un fichier S3 vers un chemin local"""
#     s3 = boto3.client("s3")
#     os.makedirs(os.path.dirname(local_path), exist_ok=True)
#     try:
#         s3.download_file(bucket, key, local_path)
#         print(f"✅ Fichier téléchargé : s3://{bucket}/{key}")
#     except Exception as e:
#         print(f"❌ Erreur de téléchargement : {e}")
#         raise

# def upload_to_s3(local_path: str, bucket: str, key: str):
#     """Upload un fichier local vers S3"""
#     s3 = boto3.client("s3")
#     try:
#         s3.upload_file(local_path, bucket, key)
#         print(f"✅ Upload terminé : s3://{bucket}/{key}")
#     except Exception as e:
#         print(f"❌ Erreur d'upload : {e}")
#         raise

# def train_model(local_csv_path: str, local_model_path: str):
#     """Entraîne un modèle de recommandation simple"""
#     df = pd.read_csv(local_csv_path)
#     df["full_text"] = (df["title"].fillna('') + " " + df["overview"].fillna('')).str.lower()

#     vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)
#     tfidf_matrix = vectorizer.fit_transform(df["full_text"])

#     model_data = {
#         "vectorizer": vectorizer,
#         "tfidf_matrix": tfidf_matrix,
#         "movie_titles": df["title"].tolist()
#     }

#     os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
#     joblib.dump(model_data, local_model_path)
#     print(f"✅ Modèle sauvegardé localement : {local_model_path}")

# if __name__ == "__main__":
#     # Charger le fichier de configuration
#     config = yaml.safe_load(open("../params.yaml"))
#     train_config = config["train"]
#     aws_config = config["aws"]

#     # Définir les credentials AWS comme variables d'environnement
#     os.environ["AWS_ACCESS_KEY_ID"] = aws_config["aws_access_key_id"]
#     os.environ["AWS_SECRET_ACCESS_KEY"] = aws_config["aws_secret_access_key"]
#     os.environ["AWS_DEFAULT_REGION"] = aws_config["region_name"]

#     # Préparer chemins
#     bucket_name = "mlopsdemlbucket21032"
#     s3_data_key = train_config["data"]
#     s3_model_key = train_config["model_s3_path"]

#     local_data_path = "../data/processed/movies_clean.csv"
#     local_model_path = "../models/model.pkl"

#     # Télécharger les données depuis S3
#     download_from_s3(bucket_name, s3_data_key, local_data_path)

#     # Entraîner le modèle
#     train_model(local_data_path, local_model_path)

#     # Uploader le modèle entraîné
#     upload_to_s3(local_model_path, bucket_name, s3_model_key)




# import os
# import yaml
# import boto3
# import joblib
# import pandas as pd
# from urllib.parse import urlparse
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report


# def download_from_s3(bucket: str, key: str, local_path: str):
#     s3 = boto3.client("s3")
#     os.makedirs(os.path.dirname(local_path), exist_ok=True)
#     try:
#         s3.download_file(bucket, key, local_path)
#         print(f"✅ Fichier téléchargé : s3://{bucket}/{key}")
#     except Exception as e:
#         print(f"❌ Erreur de téléchargement : {e}")
#         raise


# def train_model(local_csv_path: str, local_model_path: str):
#     df = pd.read_csv(local_csv_path, sep="\t")
#     df = df.dropna(subset=["NOMPL", "SEXE"])

#     X = df["NOMPL"].astype(str)
#     y = df["SEXE"].astype(str)

#     # Utilisation des n-grammes de caractères (très utile pour les noms)
#     vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
#     X_vect = vectorizer.fit_transform(X)

#     X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

#     model = LogisticRegression(max_iter=1000)
#     model.fit(X_train, y_train)

#     y_pred = model.predict(X_test)

#     print("✅ Rapport de classification :")
#     print(classification_report(y_test, y_pred))

#     os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
#     joblib.dump({"vectorizer": vectorizer, "model": model}, local_model_path)
#     print(f"✅ Modèle sauvegardé localement : {local_model_path}")


# if __name__ == "__main__":
#     # Lire la configuration
#     config = yaml.safe_load(open("../params.yaml"))
#     train_config = config["train"]
#     aws_config = config["aws"]

#     # Configurer les variables d'environnement AWS (optionnel si vous utilisez AWS CLI ou profil configuré)
#     os.environ["AWS_ACCESS_KEY_ID"] = aws_config["aws_access_key_id"]
#     os.environ["AWS_SECRET_ACCESS_KEY"] = aws_config["aws_secret_access_key"]
#     os.environ["AWS_DEFAULT_REGION"] = aws_config["region_name"]

#     # Chemins
#     bucket_name = "mlopsdemlbucket21032"
#     s3_data_key = train_config["data"]
#     local_data_path = "../data/processed/names_mr.csv"
#     local_model_path = "../models/name_gender_model.pkl"

#     # Télécharger les données puis entraîner le modèle
#     download_from_s3(bucket_name, s3_data_key, local_data_path)
#     train_model(local_data_path, local_model_path)



# import os
# import yaml
# import boto3
# import joblib
# import pandas as pd
# import mlflow
# from urllib.parse import urlparse
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score
# from mlflow.models import infer_signature

# def download_from_s3(bucket: str, key: str, local_path: str):
#     s3 = boto3.client("s3")
#     response = s3.get_object(Bucket=bucket, Key=key)
#     content = response['Body'].read()

#     os.makedirs(os.path.dirname(local_path), exist_ok=True)
#     with open(local_path, 'wb') as f:
#         f.write(content)

#     print(f"✅ Fichier téléchargé avec get_object : s3://{bucket}/{key}")

# def upload_to_s3(local_path: str, bucket: str, key: str):
#     s3 = boto3.client("s3")
#     s3.upload_file(local_path, bucket, key)
#     print(f"✅ Modèle uploadé sur : s3://{bucket}/{key}")

# def train(local_data_path, local_model_path, s3_model_path, mlflow_uri, random_state, max_iter):
#     df = pd.read_csv(local_data_path)
#     df["prenom"] = df["NOMPL"].str.strip().str.split().str[0]
#     X = df["prenom"]
#     y = df["SEXE"]

#     vectorizer = CountVectorizer(analyzer="char", ngram_range=(2, 4))
#     X_vec = vectorizer.fit_transform(X)

#     X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=random_state)

#     model = LogisticRegression(max_iter=max_iter)

#     mlflow.set_tracking_uri(mlflow_uri)
#     mlflow.set_experiment("name_gender_classifier")

#     with mlflow.start_run():
#         model.fit(X_train, y_train)
#         y_pred = model.predict(X_test)
#         acc = accuracy_score(y_test, y_pred)

#         mlflow.log_param("model", "LogisticRegression")
#         mlflow.log_param("vectorizer", "CountVectorizer(char, ngram 2-4)")
#         mlflow.log_param("max_iter", max_iter)
#         mlflow.log_metric("accuracy", acc)

#         signature = infer_signature(X_train, y_train)
#         mlflow.sklearn.log_model(model, "model", signature=signature)

#         print(f"✅ Accuracy: {acc:.4f}")

#     os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
#     joblib.dump({"model": model, "vectorizer": vectorizer}, local_model_path)
#     print(f"✅ Modèle sauvegardé localement : {local_model_path}")

#     parsed = urlparse("s3://" + s3_model_path if not s3_model_path.startswith("s3://") else s3_model_path)
#     upload_to_s3(local_model_path, parsed.netloc, parsed.path.lstrip("/"))

# if __name__ == "__main__":
#     config = yaml.safe_load(open("../params.yaml"))
#     train_config = config["train"]
#     aws_config = config["aws"]
#     mlflow_config = config["mlflow"]

#     # Commentez ou supprimez ces lignes qui forcent les mauvais credentials :
#     # os.environ["AWS_ACCESS_KEY_ID"] = aws_config["aws_access_key_id"]
#     # os.environ["AWS_SECRET_ACCESS_KEY"] = aws_config["aws_secret_access_key"]
    
#     # Gardez seulement la région si nécessaire :
#     os.environ["AWS_DEFAULT_REGION"] = aws_config["region_name"]

#     bucket_name = "mlopsdemlbucket21032"
#     s3_data_key = train_config["data"]
#     s3_model_folder = train_config["model_s3_folder"]
#     s3_model_filename = train_config["model_s3_path"]
#     s3_model_key = f"{s3_model_folder}/{s3_model_filename}"

#     local_data_path = "../data/names_clean.csv"
#     local_model_path = "../models/name_gender_model.pkl"

#     download_from_s3(bucket_name, s3_data_key, local_data_path)

#     train(
#         local_data_path,
#         local_model_path,
#         bucket_name,  
#         s3_model_key,
#         mlflow_config["MLFLOW_TRACKING_URI"],
#         train_config["random_state"],
#         train_config["max_iterations"]
#     )



import os
import yaml
import boto3
import joblib
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature

def download_from_s3(bucket: str, key: str, local_path: str):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read()

    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, 'wb') as f:
        f.write(content)

    print(f"✅ Fichier téléchargé avec get_object : s3://{bucket}/{key}")

def upload_to_s3(local_path: str, bucket: str, key: str):
    s3 = boto3.client("s3")
    s3.upload_file(local_path, bucket, key)
    print(f"✅ Modèle uploadé sur : s3://{bucket}/{key}")

def train(local_data_path, local_model_path, bucket_name, s3_model_key, mlflow_uri, random_state, max_iter):
    df = pd.read_csv(local_data_path)
    df["prenom"] = df["NOMPL"].str.strip().str.split().str[0]
    X = df["prenom"]
    y = df["SEXE"]

    vectorizer = CountVectorizer(analyzer="char", ngram_range=(2, 4))
    X_vec = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=random_state)

    model = LogisticRegression(max_iter=max_iter)

    mlflow.set_tracking_uri(mlflow_uri)
    mlflow.set_experiment("name_gender_classifier")

    with mlflow.start_run():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        mlflow.log_param("model", "LogisticRegression")
        mlflow.log_param("vectorizer", "CountVectorizer(char, ngram 2-4)")
        mlflow.log_param("max_iter", max_iter)
        mlflow.log_metric("accuracy", acc)

        signature = infer_signature(X_train, y_train)
        mlflow.sklearn.log_model(model, "model", signature=signature)

        print(f"✅ Accuracy: {acc:.4f}")

    os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
    joblib.dump({"model": model, "vectorizer": vectorizer}, local_model_path)
    print(f"✅ Modèle sauvegardé localement : {local_model_path}")

    # CORRECTION : Utilisation directe du bucket et de la clé
    upload_to_s3(local_model_path, bucket_name, s3_model_key)

if __name__ == "__main__":
    config = yaml.safe_load(open("../params.yaml"))
    train_config = config["train"]
    aws_config = config["aws"]
    mlflow_config = config["mlflow"]

    # Gardez seulement la région
    os.environ["AWS_DEFAULT_REGION"] = aws_config["region_name"]

    # CORRECTION : Utilisation du bon bucket depuis le config
    bucket_name = train_config["bucket"]  # mlopsdemlbucket21032
    s3_data_key = train_config["data"]
    s3_model_folder = train_config["model_s3_folder"]
    s3_model_filename = train_config["model_s3_path"]
    
    # CORRECTION : Construction correcte du chemin S3
    s3_model_key = f"{s3_model_folder}/{s3_model_filename}"

    local_data_path = "../data/names_clean.csv"
    local_model_path = "../models/name_gender_model.pkl"


    download_from_s3(bucket_name, s3_data_key, local_data_path)

    train(
        local_data_path,
        local_model_path,
        bucket_name,
        s3_model_key,
        mlflow_config["MLFLOW_TRACKING_URI"],  # CORRECTION : Argument positionnel
        train_config["random_state"],
        train_config["max_iterations"]
    )