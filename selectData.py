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
    inputLoc = [0, 0] # Temporal
    inputAge = 0 # Temporal
    
    groupByDist = [] # top 20 closest id 
    selectByDist(data, inputLoc, groupByDist)
    
    groupByAge = []
    selectByAge(groupByDist, inputAge, groupByAge)

# Select data by (lat, long)
def selectByDist(data, inputLoc, groupByDist):
    dist = []
    for idx,item in data.iterrows():
        tmpLoc = [float(item['x座標']),float(item['y座標'])]
        tmpDist = math.dist(tmpLoc, inputLoc)
        dist.append(tmpDist)
    dist = np.array(dist)
    groupByDist = np.argpartition(dist,20)
    groupByDist = data.iloc[groupByDist[:20]]
    
# Select data by house age 
def selectByAge(data, inputAge, groupByAge):
    age = []
    for idx,item in data.iterrows():
        tmpage = item['house_age']
        tmp = abs(tmpage - inputAge)
        age.append(tmp)
    age = np.array(age)
    groupByAge = np.argpartition(age, 10)
    groupByAge = data.iloc[groupByAge[:10]]
    
# Select data by floor area ratio

# Select data by floor numbers

# Select data by parking

# Select data by land transfer