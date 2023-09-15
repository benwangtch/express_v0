import lightgbm as lgb
import pandas as pd
import joblib

def inference(type,inferenceData):
    inferencePricePin = inferenceData['price_pin']
    inferenceData.to_csv('./sample.csv')
    inferenceData = inferenceData.drop('price_pin')
    if type == 'apartment':
        type = '公寓'
    elif type == 'building':
        type = '大樓'
    else:
        type = '透天厝'
    gbm = lgb.LGBMRegressor(n_jobs=20, 
                        n_estimators=1000, 
                        learning_rate = 0.01, 
                        # num_leaves = 32, 
                        
                        metric = 'mape')
    gbm = joblib.load(f'./lgbm/{type}all.pkl')
    pred = gbm.predict(inferenceData)
    print(inferencePricePin)
    return pred