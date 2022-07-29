import mlflow
from core.mlflow_helper import get_mlflow_client
import pandas as pd
import os
import logging
import shutil

logger = logging.getLogger(__name__)


def log_pandas_df(df_to_save, run_id):
    # Save the user generated dataset
    with open(f"{run_id}.parquet", "w+b") as temp_file:
        df_to_save.to_parquet(temp_file)
        temp_file.seek(0)
        mlflow.log_artifact(temp_file.name, f"etl_output")

    # Save some stats about the generated dataset
    df_to_save.describe().to_html(f"{run_id}_output_desc.html")
    mlflow.log_artifact(f"{run_id}_output_desc.html", f"etl_output")

    # Cleanup
    os.remove(f"{run_id}.parquet")
    os.remove(f"{run_id}_output_desc.html")

    return


def load_pandas_df(run_id: str, tracking_uri: str = None):
    # Identify correct tracking URI
    client = get_mlflow_client(tracking_uri=tracking_uri)

    # Download the artifact and read the dataset
    client.download_artifacts(run_id, f"etl_output/{run_id}.parquet", ".")
    df = pd.read_parquet(f"etl_output/{run_id}.parquet")
    shutil.rmtree("etl_output")
    return df
