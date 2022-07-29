import os
import mlflow
import logging
from contextlib import contextmanager
from mlflow.tracking import MlflowClient

logger = logging.getLogger(__name__)


def get_tracking_uri():
    return f"http://{os.environ['MLFLOW_SVC_SERVICE_HOST']}:{os.environ['MLFLOW_SVC_SERVICE_PORT']}"


def set_remote_tracking(experiment_name):
    logger.info("Setting remote mlflow tracking server")
    mlflow_host = get_tracking_uri()
    mlflow.set_tracking_uri(mlflow_host)
    mlflow.set_experiment(experiment_name)


def get_mlflow_client(tracking_uri=None):
    if tracking_uri is None:
        tracking_uri = get_tracking_uri()
    return MlflowClient(tracking_uri=tracking_uri)


@contextmanager
def start_mlflow_run(process: str, nested=False):
    """Replaces mlflow.start_run with a version that can handle exception tagging.

    Also tags the right username for the mlflow process.

    :param process: Additional tag for the process running mlflow
    :type process: str
    :param nested: Start mlflow run as a nested run
    :type nested: bool
    """
    error = True
    try:
        tags = {"Process": process}
        run = mlflow.start_run(tags=tags, nested=nested)
        yield run
    except Exception as exp:
        mlflow.set_tag("exception", str(exp))
        mlflow.set_tag("stack_trace", str(traceback.format_exc()))
        run.__exit__(type(exp), exp, exp.__traceback__)
        raise
    else:
        error = False
    finally:
        # Required to ensure exit isnt called twice
        if not error:
            run.__exit__(None, None, None)
