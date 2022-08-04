import logging
import mlflow
import pandas as pd
from core.pandas_helper import log_pandas_df, load_pandas_df
from core.mlflow_helper import start_mlflow_run
from steps.etl import get_delta_dataset, get_full_dataset
from steps.model import get_estimator_pipeline, get_feature_pipeline
import steps.model_helper as mhelper
import tempfile

logger = logging.getLogger(__name__)


def run_etl(run_on_delta: bool, config: dict):
    with start_mlflow_run(process="etl"):
        # Run the user code and get the dataset to save
        if run_on_delta:
            ds_to_save = get_delta_dataset(config)
        else:
            ds_to_save = get_full_dataset(config)

        current_run = mlflow.active_run()
        log_pandas_df(df_to_save=ds_to_save, run_id=current_run.info.run_id)


def run_train(input_data_run_id: str, config: dict):
    logger.info("Starting MLFlow experiment for training")
    with start_mlflow_run(process="train"):
        mlflow.sklearn.autolog(log_input_examples=True)

        # Read the input datasets
        dataset = load_pandas_df(run_id=input_data_run_id)

        estimator = get_estimator_pipeline(config)

        # Isolate target
        target = mhelper.get_target(raw_dataset=dataset, config=config)
        dataset = mhelper.drop_target(dataset, config)

        # Subselect features
        dataset = mhelper.subselect_features(dataset, config)

        # Split dataset
        split_dataset = mhelper.split_dataset(dataset, target, config=config)

        # Fit model and save
        estimator.fit(split_dataset["features_train"], split_dataset["target_train"])

        mlflow.sklearn.log_model(sk_model=estimator, artifact_path="estimator")


def run_prediction(input_data_run_id: str, model_run_id: str, config: dict):
    logger.info("Starting MLFlow experiment for prediction")
    with start_mlflow_run(process="predict"):
        # Retrieve the model
        model = mlflow.sklearn.load_model(f"runs:/{model_run_id}/estimator")

        # Load the input data
        input_data = load_pandas_df(run_id=input_data_run_id)
        input_data = mhelper.subselect_features(input_data, config)

        # Make a prediction
        prediction = model.predict(input_data)

        # Log the prediction
        current_run = mlflow.active_run()
        prediction_df = pd.DataFrame(prediction, columns=["prediction"])
        log_pandas_df(df_to_save=prediction_df, run_id=current_run.info.run_id)
