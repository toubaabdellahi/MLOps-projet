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
    print(f"✅ Upload S3 : s3://{bucket}/{key}")

def train(local_data_path, local_model_path, local_vectorizer_path, bucket_name, s3_model_key, s3_vectorizer_key, mlflow_uri, random_state, max_iter):
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
    joblib.dump(model, local_model_path)
    joblib.dump(vectorizer, local_vectorizer_path)

    print(f"✅ Modèle sauvegardé localement : {local_model_path}")
    print(f"✅ Vectorizer sauvegardé localement : {local_vectorizer_path}")

    upload_to_s3(local_model_path, bucket_name, s3_model_key)
    upload_to_s3(local_vectorizer_path, bucket_name, s3_vectorizer_key)

if __name__ == "__main__":
    config = yaml.safe_load(open("../params.yaml"))
    train_config = config["train"]
    aws_config = config["aws"]
    mlflow_config = config["mlflow"]

    os.environ["AWS_DEFAULT_REGION"] = aws_config["region_name"]

    bucket_name = train_config["bucket"]
    s3_data_key = train_config["data"]
    s3_model_folder = train_config["model_s3_folder"]
    s3_model_filename = train_config["model_s3_path"]
    s3_vectorizer_filename = "name_gender_vectorizer.pkl"

    s3_model_key = f"{s3_model_folder}/{s3_model_filename}"
    s3_vectorizer_key = f"{s3_model_folder}/{s3_vectorizer_filename}"

    local_data_path = "../data/names_clean.csv"
    local_model_path = "../models/name_gender_model.pkl"
    local_vectorizer_path = "../models/name_gender_vectorizer.pkl"

    download_from_s3(bucket_name, s3_data_key, local_data_path)

    train(
        local_data_path,
        local_model_path,
        local_vectorizer_path,
        bucket_name,
        s3_model_key,
        s3_vectorizer_key,
        mlflow_config["MLFLOW_TRACKING_URI"],
        train_config["random_state"],
        train_config["max_iterations"]
    )
