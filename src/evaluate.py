import os
import yaml
import boto3
import joblib
import pandas as pd
import mlflow
from sklearn.metrics import accuracy_score
from botocore.exceptions import ClientError, NoCredentialsError

def setup_aws_credentials(aws_cfg):
    """Setup AWS credentials with session token support"""
    try:
        # Set environment variables
        os.environ["AWS_ACCESS_KEY_ID"] = aws_cfg["aws_access_key_id"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = aws_cfg["aws_secret_access_key"]
        os.environ["AWS_DEFAULT_REGION"] = aws_cfg["region_name"]
        
        # Add session token 
        if "aws_session_token" in aws_cfg:
            os.environ["AWS_SESSION_TOKEN"] = aws_cfg["aws_session_token"]
            print(" Using temporary AWS credentials with session token")
        else:
            print(" Using permanent AWS credentials")
        
        # Test credentials
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f" AWS Identity verified: {identity.get('UserId', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f" AWS credentials setup failed: {e}")
        print("\nPlease check:")
        print("1. Your AWS credentials are valid and not expired")
        print("2. Include aws_session_token in params.yaml if using temporary credentials")
        print("3. Your AWS region is correct")
        return False

def download_from_s3(bucket, key, local_path):
    """Download file from S3 with comprehensive error handling"""
    try:
        s3 = boto3.client("s3")
        
        print(f" Attempting to download s3://{bucket}/{key}")
        
        # Check if file exists first
        try:
            s3.head_object(Bucket=bucket, Key=key)
            print(f" File exists in S3")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f" File not found: s3://{bucket}/{key}")
                print("Please check the file path in your params.yaml")
                return False
            elif error_code == '403':
                print(f" Access denied to: s3://{bucket}/{key}")
                print("Please check your AWS permissions")
                return False
            else:
                print(f" Error checking file: {e}")
                return False
        
        # Create local directory
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Download the file
        s3.download_file(bucket, key, local_path)
        print(f" Downloaded to: {local_path}")
        
        # Verify download
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            print(f" File verified: {os.path.getsize(local_path)} bytes")
            return True
        else:
            print(f" Download verification failed")
            return False
            
    except Exception as e:
        print(f" Download failed: {e}")
        return False

def evaluate(data_path, model_path, mlflow_uri):
    """Evaluate the model with error handling"""
    try:
        print(f"\n Starting evaluation...")
        
        # Load and prepare data
        print(f" Loading data from: {data_path}")
        df = pd.read_csv(data_path)
        print(f" Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Data preprocessing
        df["prenom"] = df["NOMPL"].str.strip().str.split().str[0]
        X = df["prenom"]
        y = df["SEXE"]
        
        print(f"  Data prepared: {len(X)} samples")
        print(f"   - Unique names: {X.nunique()}")
        print(f"   - Gender distribution: {y.value_counts().to_dict()}")
        
        # Load model
        print(f" Loading model from: {model_path}")
        model_bundle = joblib.load(model_path)
        vectorizer = model_bundle["vectorizer"]
        model = model_bundle["model"]
        print(f" Model loaded successfully")
        
        # Make predictions
        print(f" Making predictions...")
        X_vec = vectorizer.transform(X)
        y_pred = model.predict(X_vec)
        
        # Calculate metrics
        acc = accuracy_score(y, y_pred)
        print(f" Accuracy calculated: {acc:.4f}")
        
        # Log to MLflow
        print(f" Logging to MLflow...")
        mlflow.set_tracking_uri(mlflow_uri)
        mlflow.set_experiment("name_gender_classifier")
        
        with mlflow.start_run(run_name="evaluation"):
            mlflow.log_metric("eval_accuracy", acc)
            mlflow.log_param("eval_samples", len(X))
            mlflow.log_param("unique_names", X.nunique())
            
            # Log some sample predictions
            sample_results = pd.DataFrame({
                'name': X.head(10),
                'actual': y.head(10),
                'predicted': y_pred[:10]
            })
            print(f"\n Sample predictions:")
            print(sample_results.to_string(index=False))
        
        print(f"\n Evaluation completed successfully!")
        print(f" Final Accuracy: {acc:.4f}")
        
        return acc
        
    except Exception as e:
        print(f" Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function with comprehensive error handling"""
    try:
        print(" Starting Name Gender Model Evaluation")
        print("=" * 50)
        
        # Load configuration
        print(" Loading configuration...")
        config = yaml.safe_load(open("../params.yaml"))
        train_cfg = config["train"]
        aws_cfg = config["aws"]
        mlflow_cfg = config["mlflow"]
        print(" Configuration loaded")
        
        # Setup AWS credentials
        print("\n Setting up AWS credentials...")
        if not setup_aws_credentials(aws_cfg):
            print(" Exiting due to AWS credentials error")
            return
        
        # Define paths
        bucket = train_cfg["bucket"]
        data_key = train_cfg["data"]
        model_key = f"{train_cfg['model_s3_folder']}/{train_cfg['model_s3_path']}"
        
        local_data = "../data/names_eval.csv"
        local_model = "../models/name_gender_model.pkl"
        
        print(f"\n File paths:")
        print(f"   Data: s3://{bucket}/{data_key}")
        print(f"   Model: s3://{bucket}/{model_key}")
        
        # Download files
        print(f"\n Downloading files from S3...")
        
        if not download_from_s3(bucket, data_key, local_data):
            print(" Failed to download data file")
            return
            
        if not download_from_s3(bucket, model_key, local_model):
            print(" Failed to download model file")
            return
        
        # Run evaluation
        print(f"\n Running evaluation...")
        accuracy = evaluate(local_data, local_model, mlflow_cfg["MLFLOW_TRACKING_URI"])
        
        if accuracy is not None:
            print(f"\n Evaluation completed successfully!")
            print(f" Model Accuracy: {accuracy:.4f}")
        else:
            print(f"\n Evaluation failed")
            
    except Exception as e:
        print(f" Main execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()