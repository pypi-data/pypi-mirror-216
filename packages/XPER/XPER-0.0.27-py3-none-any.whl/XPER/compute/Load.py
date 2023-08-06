import joblib

def xgboost():
    model = joblib.load('xgboost_model.joblib')
    return model
xgboost()