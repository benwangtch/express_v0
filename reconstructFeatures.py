import numpy as np
import pandas as pd
import requests
import math
from math import degrees, tan, sin, cos, radians
from convertCoord import Wsg84ToTWD97

allFeatList = ['city_nm2', 'town_nm', '交易車位', '小坪數物件', '建物型態', '主要用途', '主要建材', '有無管理組織', 
    '車位類別', '電梯', 'firstfloor_ind', 'shop_ind', 'building_type2', 'col2_ind', 'villname', 
    '都市土地使用分區', '非都市土地使用編定','土地移轉總面積(坪)','建物移轉總面積(坪)','建物現況格局-房','建物現況格局-廳','建物現況格局-衛','建物現況格局-隔間',
        '車位移轉總面積(坪)','主建物面積','附屬建物面積','陽台面積','house_age','交易筆棟數_土地','交易筆棟數_建物','交易筆棟數_停車位','building_area_no_park','single_floor_area','far','floor','total_floor',
        'x座標','y座標','larea_utilize_ratio','park_cnt_flat','park_cnt_mach',
        'n_a_10', 'n_a_50', 'n_a_100', 'n_a_250', 'n_a_500', 'n_a_1000', 'n_a_5000', 'n_a_10000','n_c_10', 'n_c_50', 'n_c_100', 'n_c_250', 'n_c_500', 'n_c_1000', 'n_c_5000', 'n_c_10000',
        'area_kilometer','population_density','house_price_index','unemployment_rate','econ_rate','lending_rate','land_tx_count','land_price','steel_id']
CatFeatList = [
    'city_nm2', 'town_nm', '交易車位', '小坪數物件', '建物型態', '主要用途', '主要建材', '有無管理組織', 
    '車位類別', '電梯', 'firstfloor_ind', 'shop_ind', 'building_type2', 'col2_ind', 'villname', 
    '都市土地使用分區', '非都市土地使用編定'
]
NumFeatList = ['土地移轉總面積(坪)','建物移轉總面積(坪)','建物現況格局-房','建物現況格局-廳','建物現況格局-衛','建物現況格局-隔間',
        '車位移轉總面積(坪)','主建物面積','附屬建物面積','陽台面積','house_age','交易筆棟數_土地','交易筆棟數_建物','交易筆棟數_停車位','building_area_no_park','single_floor_area','far','floor','total_floor',
        'x座標','y座標','larea_utilize_ratio','park_cnt_flat','park_cnt_mach',
        'n_a_10', 'n_a_50', 'n_a_100', 'n_a_250', 'n_a_500', 'n_a_1000', 'n_a_5000', 'n_a_10000','n_c_10', 'n_c_50', 'n_c_100', 'n_c_250', 'n_c_500', 'n_c_1000', 'n_c_5000', 'n_c_10000',
        'area_kilometer','population_density','house_price_index','unemployment_rate','econ_rate','lending_rate','land_tx_count','land_price','steel_id']

# Inputs: 
# Building => addr, age, area
# apartment => addr, age, total_floor, parking_area
# House => addr, age, far, land transfer, house transfer
# Fill missing feature, Numerical feature => average, Catagorical data => the most catagory
def fillMissingFeature(inputData, groupData):
    
    tmp  = pd.DataFrame(columns=allFeatList, index=[0])
    tmp['x座標'] = float(inputData['x座標'])
    tmp['y座標'] = float(inputData['y座標'])
    tmp['house_age'] = float(inputData['age'])
    
    if inputData['type'] == 'apartment':
        tmp['total_floor'] = float(inputData['floor'])
        tmp['車位移轉總面積(坪)'] = float(inputData['car'])
        # Get most common for catFeat, mean for numFeat
        for catFeat in CatFeatList:
            tmp[catFeat] = groupData[catFeat].mode()[0] 
        
        for numFeat in NumFeatList:
            if numFeat != 'x座標' and numFeat !='y座標'and numFeat !='house_age'and numFeat !='total_floor' and numFeat !='車位移轉總面積(坪)':
                tmp[numFeat] = groupData[numFeat].mean()
        
    elif inputData['type'] == 'building':
        tmp['主建物面積'] = float(inputData['area'])
        
        for catFeat in CatFeatList:
            tmp[catFeat] = groupData[catFeat].mode()[0]
            
        for numFeat in NumFeatList:
            if numFeat != 'x座標' and numFeat !='y座標'and numFeat !='house_age'and numFeat !='主建物面積':
                tmp[numFeat] = groupData[numFeat].mean()
    else: # House
        tmp['far'] = float(inputData['far'])
        tmp['土地移轉總面積(坪)'] = float(inputData['trans1'])
        
        for catFeat in CatFeatList:
            tmp[catFeat] = groupData[catFeat].mode()[0]
        for numFeat in NumFeatList:
            if numFeat != 'x座標' and numFeat !='y座標'and numFeat !='house_age'and numFeat !='far' and numFeat !='土地移轉總面積(坪)':
                tmp[numFeat] = groupData[numFeat].mean()
    return tmp

# Using google API for converting the address => (lat, lon)
def getLatLong(inputData):
    addr =inputData['addr']
    res = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key=AIzaSyCkBm3LspfsTiKQUh7EmHQV8bkwHnVFff0')
    resJson = res.json()
    resJson = resJson['results'][0]
    latlng = resJson['geometry']['location']
    # Save the lat,lng to inference data
    inputData['lat'] = latlng['lat']
    inputData['lon'] = latlng['lng']
    
    print(latlng['lat'],latlng['lng'])
    # Turn lat lon to TWD97 latlon
    lat, lng = LatLontoTwd97(latlng['lat'],latlng['lng'] )
    inputData['x座標'] = lng
    inputData['y座標'] = lat   
    print(inputData)
    return inputData

def TWD97ToLatLon(x, y):
    dx = 250000
    dy = 0
    lon0 = radians(121)
    k0 = 0.9999
    a = 6378137.0
    b = 6356752.314245
    e = math.pow((1 - math.pow(b, 2) / math.pow(a, 2)), 0.5)

    x -= dx
    y -= dy
    # Calculate the Meridional Arc
    M = y / k0
    # Calculate Footprint Latitude
    mu = M / (a * (1.0 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))
    e1 = (1.0 - math.pow((1.0 - math.pow(e, 2)), 0.5)) / (1.0 + math.pow((1.0 - math.pow(e, 2)), 0.5))

    J1 = (3 * e1 / 2 - 27 * math.pow(e1, 3) / 32.0)
    J2 = (21 * math.pow(e1, 2) / 16 - 55 * math.pow(e1, 4) / 32.0)
    J3 = (151 * math.pow(e1, 3) / 96.0)
    J4 = (1097 * math.pow(e1, 4) / 512.0)

    fp = mu + J1 * math.sin(2 * mu) + J2 * math.sin(4 * mu) + J3 * math.sin(6 * mu) + J4 * math.sin(8 * mu)
    # Calculate Latitude and Longitude
    e2 = math.pow((e * a / b), 2)
    C1 = math.pow(e2 * math.cos(fp), 2)
    T1 = math.pow(math.tan(fp), 2)
    R1 = a * (1 - math.pow(e, 2)) / math.pow((1 - math.pow(e, 2) * math.pow(math.sin(fp), 2)), (3.0 / 2.0))
    N1 = a / math.pow((1 - math.pow(e, 2) * math.pow(math.sin(fp), 2)), 0.5)

    D = x / (N1 * k0)

    # lat
    Q1 = N1 * math.tan(fp) / R1
    Q2 = (math.pow(D, 2) / 2.0)
    Q3 = (5 + 3 * T1 + 10 * C1 - 4 * math.pow(C1, 2) - 9 * e2) * math.pow(D, 4) / 24.0
    Q4 = (61 + 90 * T1 + 298 * C1 + 45 * math.pow(T1, 2) - 3 * math.pow(C1, 2) - 252 * e2) * math.pow(D, 6) / 720.0
    lat = fp - Q1 * (Q2 - Q3 + Q4)
    # long
    Q5 = D
    Q6 = (1 + 2 * T1 + C1) * math.pow(D, 3) / 6
    Q7 = (5 - 2 * C1 + 28 * T1 - 3 * math.pow(C1, 2) + 8 * e2 + 24 * math.pow(T1, 2)) * math.pow(D, 5) / 120.0
    lon = lon0 + (Q5 - Q6 + Q7) / math.cos(fp)

    return [math.degrees(lat), math.degrees(lon)]
# Formula for converting between TWD97 and WGS84

def LatLontoTwd97(x,y):
    c = Wsg84ToTWD97()
    lat = radians(float(x))
    lon = radians(float(y))
    x, y = c.convert(lat, lon)
    # tx = x/0.00000899823754
    # ty = (y-121)*math.cos(math.radians(x))/0.000008983152841195214 + 250000
    return (y, x)

def getGroupLatLon(data):
    for idx,item in data.iterrows():
        tmp = TWD97ToLatLon(item['x座標'],item['y座標'])
        data.loc[idx, 'lat'] = tmp[0]
        data.loc[idx, 'lon'] = tmp[1]
        
        res = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={tmp[0]}, {tmp[1]}&key=AIzaSyCkBm3LspfsTiKQUh7EmHQV8bkwHnVFff0')
        resJson = res.json()
        resJson = resJson['results'][0]
        addr = resJson['formatted_address'] # addr of data
        data.loc[idx, 'addr'] = addr
        print(addr)
    return data