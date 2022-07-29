from sklearn.linear_model import Lasso


def get_feature_pipeline(config: dict):
    return None


def get_estimator_pipeline(config: dict):
    model = Lasso()
    return model
