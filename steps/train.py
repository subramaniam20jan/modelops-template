def estimator_fn():
  from sklearn.linear_model import SGDRegressor

  return SGDRegressor(random_state=42)