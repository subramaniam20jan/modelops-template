from sklearn.linear_model import Lasso
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


def get_feature_pipeline(config: dict):
    return None


def get_estimator_pipeline(config: dict):
    imputer = SimpleImputer()
    model = Lasso()
    return Pipeline([("Imputer", imputer), ("Lasso", model)])
