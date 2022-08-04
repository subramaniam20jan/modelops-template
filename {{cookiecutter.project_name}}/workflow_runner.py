from core import worker, util
from core.logger import configure_logger
import typer
import logging

logger = logging.getLogger(__name__)


app = typer.Typer()

HELP = {
    "config_grid_index": "Grid index to the config to use.",
    "run_on_delta": "Run either a delta ETL load or full load",
    "input_data_run_id": "Run id of ETL flow to use as input.",
}


@app.command("train")
def train_cmd(
    input_data_run_id: str = typer.Argument(..., help=HELP["input_data_run_id"]),
    config_grid_index: int = typer.Option(-1, help=HELP["config_grid_index"]),
):
    """Command to run model training

    :param config_grid_index: _description_, defaults to -1
    :type config_grid_index: int, optional
    """
    logger.info("Training a model")

    # Setup the mlflow server and experiment
    general_config = util.load_config("workflow_conf.yaml", "general")
    configure_logger(general_config["log_config"])

    # Load config and run Training
    config = util.load_config(
        "workflow_conf.yaml", "train", grid_index=config_grid_index
    )
    worker.run_train(input_data_run_id=input_data_run_id, config=config)


@app.command("etl")
def etl_cmd(
    run_on_delta: bool = typer.Option(False, help=HELP["run_on_delta"]),
    config_grid_index: int = typer.Option(-1, help=HELP["config_grid_index"]),
):
    """Command to run ETL operations.

    :param config_grid_index: _description_, defaults to -1
    :type config_grid_index: int, optional
    """
    logger.info("Performing ETL")

    # Setup the mlflow server and experiment
    general_config = util.load_config("workflow_conf.yaml", "general")
    configure_logger(general_config["log_config"])

    # Load config and run ETL
    config = util.load_config("workflow_conf.yaml", "etl", grid_index=config_grid_index)
    worker.run_etl(run_on_delta=run_on_delta, config=config)


@app.command("predict")
def predict_cmd(model_name: str, run_id: str):
    """Command to run a model prediction

    :param model_name: Name of the model to run a prediction on
    :type model_name: str
    :param run_id: Run id of the experiment to retrive model from
    :type run_id: str
    """
    typer.echo(f"Performing prediction on {model_name} {run_id}")


if __name__ == "__main__":
    app()
