import numpy
import pandas as pd
import math 
import numpy as np

# Inputs: 
# Building => addr, age, area
# apartment => addr, age, total_floor, parking_area
# House => addr, age, far, land transfer, house transfer
def getSimilarData(inputData):
    if inputData['type'] == 'apartment':
        data = pd.read_csv('./final_inference/all_apartment.csv')
        groupNumList = [30, 20, 10, 5]
    elif inputData['type'] == 'building':
        data = pd.read_csv('./final_inference/all_building.csv')
        groupNumList = [20, 10, 5]
    else:
        data = pd.read_csv('./final_inference/all_house.csv')
        groupNumList = [30, 20, 10, 5]
        
    
    # InputData will contain a Chinese address, need to be convert to (lat, long) either TWD97 or WGS84
    
    inputLoc = [0, 0] # Temporal, need to be turn by inputData['addr']
    
    # top 30 closest id 
    groupByDist = [] 
    selectByDist(data, groupNumList[0], inputLoc, groupByDist)
    
    # Top 20 age
    groupByAge = []
    selectByAge(groupByDist, groupNumList[1], inputData['age'], groupByAge)
    
    if inputData['type'] == 'apartment':
        groupByTotalFloor = []
        selectByTotalFloor(groupByAge, groupNumList[2], inputData['floor'], groupByTotalFloor )
        
        groupByParking = []
        selectByParking(groupByTotalFloor, groupNumList[3], inputData['car'], groupByParking)
    elif inputData['type'] == 'building':
        groupByArea = []
        selectByArea(groupByAge, groupNumList[2], inputData['area'], groupByArea)
    else:
        groupByFar = []
        selectByFar(groupByAge, groupNumList[2], inputData['far'], groupByFar)
        
        groupByLandTransfer = []
        selectByLandTransfer(groupByFar, groupNumList[3], inputData['trans1'], groupByLandTransfer)
        
            

# Select data by (lat, long)
def selectByDist(data, groupNum, inputLoc, groupByDist):
    dist = []
    for idx,item in data.iterrows():
        tmpLoc = [float(item['x座標']),float(item['y座標'])]
        tmpDist = math.dist(tmpLoc, inputLoc)
        dist.append(tmpDist)
    dist = np.array(dist)
    groupByDist = np.argpartition(dist,groupNum)
    groupByDist = data.iloc[groupByDist[:groupNum]]
    
# Select data by house age 
def selectByAge(data, groupNum, inputAge, groupByAge):
    age = []
    for idx,item in data.iterrows():
        tmpAge = item['house_age']
        tmp = abs(tmpAge - inputAge)
        age.append(tmp)
    age = np.array(age)
    groupByAge = np.argpartition(age, groupNum)
    groupByAge = data.iloc[groupByAge[:groupNum]]

# Select data by building area
def selectByArea(data, groupNum, inputArea, groupByArea):
    area = []
    for idx,item in data.iterrows():
        tmpArea = item['主建物面積']
        tmp = abs(tmpArea - inputArea)
        area.append(tmp)
    area = np.array(area)
    groupByArea = np.argpartition(area, groupByArea)
    groupByArea = data.iloc[groupByArea[:groupNum]]

# Select data by floor area ratio
def selectByFar(data, groupNum, inputFar, groupByFar):
    far = []
    for idx,item in data.iterrows():
        tmpFar = item['far']
        tmp = abs(tmpFar - inputFar)
        far.append(tmp)
    far = np.array(far)
    groupByFar = np.argpartition(far, groupNum)
    groupByFar = data.iloc[groupByFar[:groupNum]]
    
# Select data by total floor
def selectByTotalFloor(data, groupNum, inputTotalFloor, groupByTotalFloor):
    totalFloor = []
    for idx,item in data.iterrows():
        tmpTotalFloor = item['total_floor']
        tmp = abs(tmpTotalFloor - inputTotalFloor)
        totalFloor.append(tmp)
    totalFloor = np.array(totalFloor)
    groupByTotalFloor = np.argpartition(totalFloor, groupNum)
    groupByTotalFloor = data.iloc[groupByTotalFloor[:groupNum]]
    
# Select data by parking
def selectByParking(data, groupNum, inputParking, groupByParking):
    parking = []
    for idx,item in data.iterrows():
        tmpParking = item['車位移轉總面積(坪)']
        tmp = abs(tmpParking - inputParking)
        parking.append(tmp)
    parking = np.array(parking)
    groupByParking = np.argpartition(parking, groupNum)
    groupByParking = data.iloc[groupByParking[:groupNum]]
    
# Select data by land transfer
def selectByLandTransfer(data, groupNum, inputLandTransfer, groupByLandTransfer):
    landTransfer = []
    for idx,item in data.iterrows():
        tmpLandTransfer = item['土地移轉總面積(坪)']
        tmp = abs(tmpLandTransfer - inputLandTransfer)
        landTransfer.append(tmp)
    landTransfer = np.append(landTransfer)
    groupByLandTransfer = np.argpartition(landTransfer, groupNum)
    groupByLandTransfer = data.iloc[groupByLandTransfer[:groupNum]]