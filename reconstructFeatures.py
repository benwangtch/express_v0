import numpy as np
import pandas as pd
import math 

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
    tmp['x座標'] = inputData['x座標']
    tmp['y座標'] = inputData['y座標']
    tmp['house_age'] = inputData['age']
    
    if inputData['type'] == 'apartment':
        tmp['total_floor'] = inputData['floor']
        tmp['車位移轉總面積(坪)'] = inputData['car']
        # Get most common for catFeat, mean for numFeat
        for catFeat in CatFeatList:
            tmp[catFeat] = groupData[catFeat].mode()[0] 
        
        for numFeat in NumFeatList:
            if numFeat != 'total_floor' or '車位移轉總面積(坪)':
                tmp[numFeat] = groupData[numFeat].mean()
        
    elif inputData['type'] == 'building':
        tmp['主建物面積'] = inputData['area']
        
        for catFeat in CatFeatList:
            tmp[catFeat] = groupData[catFeat].mode()[0]
            
        for numFeat in NumFeatList:
            if numFeat != '主建物面積':
                tmp[numFeat] = groupData[numFeat].mean()
    else: # House
        tmp['far'] = inputData['far']
        tmp['土地移轉總面積(坪)'] = inputData['trans1']
        
        for catFeat in CatFeatList:
            tmp[catFeat] = groupData[catFeat].mode()[0]
        for numFeat in NumFeatList:
            if numFeat != 'far' or '土地移轉總面積(坪)':
                tmp[numFeat] = groupData[numFeat].mean()
    return tmp

def getLatLong():
    pass