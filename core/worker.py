import mlflow
from core.pandas_helper import log_pandas_df, load_pandas_df
from core.mlflow_helper import start_mlflow_run
from steps.etl import get_delta_dataset, get_full_dataset
from steps.model import get_estimator_pipeline, get_feature_pipeline
import steps.model_helper as mhelper
import tempfile


def run_etl(run_on_delta: bool, config: dict):
    with start_mlflow_run(process="etl"):
        # Run the user code and get the dataset to save
        if run_on_delta:
            ds_to_save = get_delta_dataset(config)
        else:
            ds_to_save = get_full_dataset(config)

        current_run = mlflow.active_run()
        log_pandas_df(df_to_save=ds_to_save, run_id=current_run.info.run_id)


def run_train(input_data_run_id: list, config: dict):
    with start_mlflow_run(process="train"):
        # Read the input datasets
        dataset = load_pandas_df(run_id=input_data_run_id)

        estimator = get_estimator_pipeline(config)
        target_name = mhelper.get_target(raw_dataset=dataset, config=config)
        split_dataset = mhelper.split_dataset(
            dataset, dataset[target_name], config=config
        )
        dataset = mhelper.drop_target(dataset, config)

        # Fit model and save
        estimator.fit(dataset["features_train"], dataset["target_train"])
        mlflow.sklearn.save_model(estimator, path="estimator")
