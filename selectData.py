import numpy
import pandas as pd
import math 
import numpy as np

def getSimilarData(inputData):
    if inputData['type'] == 'apartment':
        data = pd.read_csv('./final_inference/lgbm_公寓.csv')
    elif inputData['type'] == 'building':
        data = pd.read_csv('./final_inference/lgbm_大樓.csv')
    else:
        data = pd.read_csv('./final_inference/lgbm_透天厝.csv')
        
    # InputData will contain a Chinese address, need to be convert to (lat, long) either TWD97 or WGS84
    inputLoc = [0, 0]
    
    dist = []
    for idx,item in data.iterrows():
        tmpLoc = [float(item['x座標']),float(item['y座標'])]
        tmpDist = math.dist(tmpLoc, inputLoc)
        dist.append(tmpDist)
    dist = np.array(dist)
    idxDist = np.argpartition(dist,20)
    
def selectByDist():
    pass