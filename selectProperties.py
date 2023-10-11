import numpy
import pandas as pd
import math 
import numpy as np

# Inputs: 
# Building => addr, age, area
# apartment => addr, age, total_floor, parking_area
# House => addr, age, far, land transfer, house transfer
# inputData = {'type':building, 'x座標':0, 'y座標':0, 'house_age':10,...}
def getSimilarProperties(inputData):
    """Get the most similar datas by parameter filtering, base on different property type input features.

    Args:
        inputData (json): The original inputData with converted coordinates for calculating the distances.

    Returns:
        DataFrame: Returns the most similar five data after filtering.
    """
    if inputData['type'] == 'apartment':
        data = pd.read_csv('./data/all_apartment.csv')
        groupNumList = [30, 20, 10, 5]
    elif inputData['type'] == 'building':
        data = pd.read_csv('./data/all_building.csv')
        groupNumList = [20, 6, 5]
    else:
        data = pd.read_csv('./data/all_house.csv')
        groupNumList = [30, 20, 10, 5]
        
    # InputData will contain a Chinese address, need to be convert to (lat, long) either TWD97 or WGS84
    groupByDist = []
    groupByDist = selectByDist(data, groupNumList[0], [inputData['x座標'], inputData['y座標']], groupByDist)
    
    groupByAge = []
    groupByAge = selectByAge(groupByDist, groupNumList[1], inputData['age'], groupByAge)
    
    if inputData['type'] == 'apartment':
        # Convert the features taken log while training
        inputData['car'] = take_log(inputData['car'])
        groupByTotalFloor = []
        groupByTotalFloor = selectByTotalFloor(groupByAge, groupNumList[2], inputData['floor'], groupByTotalFloor )
        
        groupByParking = []
        groupByParking = selectByParking(groupByTotalFloor, groupNumList[3], inputData['car'], groupByParking)
        return groupByParking
    elif inputData['type'] == 'building':
        # Convert the features taken log while training
        inputData['area'] = take_log(inputData['area'])
        groupByArea = []
        groupByArea = selectByArea(groupByAge, groupNumList[2], inputData['area'], groupByArea)
        return groupByArea
    else:
        # Convert the features taken log while training
        inputData['trans1'] = take_log(inputData['trans1'])
        inputData['trans2'] = take_log(inputData['trans2'])
        groupByFar = []
        groupByFar = selectByFar(groupByAge, groupNumList[2], inputData['far'], groupByFar)
        
        groupByLandTransfer = []
        groupByLandTransfer = selectByLandTransfer(groupByFar, groupNumList[3], inputData['trans1'], groupByLandTransfer)
        return groupByLandTransfer
        
def take_log(x):
    x = float(x)
    if x>0:
        return math.log(x)
    else:
        return 0.  
           

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
    return groupByDist
    
# Select data by house age 
def selectByAge(data, groupNum, inputAge, groupByAge):
    age = []
    inputAge = float(inputAge)
    for idx,item in data.iterrows():
        tmpAge = item['house_age']
        tmp = abs(tmpAge - inputAge)
        age.append(tmp)
    age = np.array(age)
    groupByAge = np.argpartition(age, groupNum)
    groupByAge = data.iloc[groupByAge[:groupNum]]
    return groupByAge
# Select data by building area
def selectByArea(data, groupNum, inputArea, groupByArea):
    area = []
    inputArea = float(inputArea)
    for idx,item in data.iterrows():
        tmpArea = float(item['主建物面積'])
        tmp = abs(tmpArea - inputArea)
        area.append(tmp)
    area = np.array(area)
    groupByArea = np.argpartition(area, groupNum)
    groupByArea = data.iloc[groupByArea[:groupNum]]
    return groupByArea
# Select data by floor area ratio
def selectByFar(data, groupNum, inputFar, groupByFar):
    far = []
    inputFar = float(inputFar)
    for idx,item in data.iterrows():
        tmpFar = item['far']
        tmp = abs(tmpFar - inputFar)
        far.append(tmp)
    far = np.array(far)
    groupByFar = np.argpartition(far, groupNum)
    groupByFar = data.iloc[groupByFar[:groupNum]]
    return groupByFar
# Select data by total floor
def selectByTotalFloor(data, groupNum, inputTotalFloor, groupByTotalFloor):
    totalFloor = []
    inputTotalFloor = float(inputTotalFloor)
    for idx,item in data.iterrows():
        tmpTotalFloor = item['total_floor']
        tmp = abs(tmpTotalFloor - inputTotalFloor)
        totalFloor.append(tmp)
    totalFloor = np.array(totalFloor)
    groupByTotalFloor = np.argpartition(totalFloor, groupNum)
    groupByTotalFloor = data.iloc[groupByTotalFloor[:groupNum]]
    return groupByTotalFloor
# Select data by parking
def selectByParking(data, groupNum, inputParking, groupByParking):
    parking = []
    inputParking = float(inputParking)
    for idx,item in data.iterrows():
        tmpParking = item['車位移轉總面積(坪)']
        tmp = abs(tmpParking - inputParking)
        parking.append(tmp)
    parking = np.array(parking)
    groupByParking = np.argpartition(parking, groupNum)
    groupByParking = data.iloc[groupByParking[:groupNum]]
    return groupByParking
# Select data by land transfer
def selectByLandTransfer(data, groupNum, inputLandTransfer, groupByLandTransfer):
    landTransfer = []
    inputLandTransfer = float(inputLandTransfer)
    for idx,item in data.iterrows():
        tmpLandTransfer = item['土地移轉總面積(坪)']
        tmp = abs(tmpLandTransfer - inputLandTransfer)
        landTransfer.append(tmp)
    landTransfer = np.array(landTransfer)
    groupByLandTransfer = np.argpartition(landTransfer, groupNum)
    groupByLandTransfer = data.iloc[groupByLandTransfer[:groupNum]]
    return groupByLandTransfer
def take_exp(x):
    x = float(x)
    if x > 0:
        return math.exp(x)
    else:
        return 0
def convertGroupNumFeat(type, groupData):
        groupData['車位移轉總面積(坪)'] = groupData['車位移轉總面積(坪)'].apply(take_exp)
        groupData['主建物面積'] = groupData['主建物面積'].apply(take_exp)
        
        groupData['土地移轉總面積(坪)'] = groupData['土地移轉總面積(坪)'].apply(take_exp)
        groupData['建物移轉總面積(坪)'] = groupData['建物移轉總面積(坪)'].apply(take_exp)
        return groupData