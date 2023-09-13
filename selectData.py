import numpy
import pandas as pd
import math 

def getSimilarData(inputData):
    if inputData['type'] == 'apartment':
        data = pd.read_csv('./final_inference/lgbm_公寓.csv')
    elif inputData['type'] == 'building':
        data = pd.read_csv('./final_inference/lgbm_大樓.csv')
    else:
        data = pd.read_csv('./final_inference/lgbm_透天厝.csv')
        
    # InputData will contain a Chinese address, need to be convert to (lat, long) either TWD97 or WGS84