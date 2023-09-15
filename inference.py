import lightgbm as lgb
import pandas as pd
import joblib

def inference(type,inferenceData):
    gbm = lgb.LGBMRegressor(n_jobs=20, 
                        n_estimators=1000, 
                        learning_rate = 0.01, 
                        # num_leaves = 32, 
                        
                        metric = 'mape')
    gbm = joblib.load(f'./lgbm/{type}all.pkl')
       