import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random 
import lightgbm as lgb
import pandas as pd
import argparse
import time
from utils import predAndCalScore, checkAndMakeDir, initReport, addItemToReport, gridSearch, column_filter
# from data import dataset
import joblib
# Configs
parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str)
args  = parser.parse_args()
mode = args.type
get_time = False # for cal inference time
random.seed(18)
DataPath = f'./data/demo_paper_data/'
appData= True # for app demo

if appData:
    train_Feat = pd.read_csv(f'{DataPath}{mode}_trainFeat.csv')# For app demo
    val_Feat= pd.read_csv(f'{DataPath}{mode}_valFeat.csv')# For app demo
    test_Feat = pd.read_csv(f'{DataPath}{mode}_testFeat.csv')
    train_Price = pd.read_csv(f'{DataPath}{mode}_trainPrice.csv')# For app demo
    val_Price = pd.read_csv(f'{DataPath}{mode}_valPrice.csv')# For app demo
    test_Price = pd.read_csv(f'{DataPath}{mode}_testPrice.csv')# For app demo
    
    train_Feat=  column_filter(train_Feat)# For app demo
    val_Feat = column_filter(val_Feat)# For app demo
    test_Feat = column_filter(test_Feat)
    
    train_Feat = pd.concat([train_Feat, val_Feat])# For app demo
    train_Price = pd.concat([train_Price, val_Price])# For app demo
    test_Feat = pd.concat([train_Feat, test_Feat]) # For app demo
    test_Price = pd.concat([train_Price, test_Price])# For app demo
# load dataset
# Starting predicting...
print('Loading dataset...')

# test_feat = pd.read_csv(f'./data/demo_paper_data/{mode}_testFeat.csv')
# test_Price = pd.read_csv(f'./data/demo_paper_data/{mode}_testPrice.csv').values.reshape(-1)
test_Price = test_Price.values.reshape(-1)

if get_time:
    test_Feat = test_Feat.iloc[0:1]
    test_Price = test_Price[0]
# Preprocess dataset
total_inf = 0
start_time= time.time()
# test_feat = column_filter(test_Feat)
end_time = time.time()
total_inf += round(end_time - start_time, 5)

gbm = lgb.LGBMRegressor(n_jobs=20, 
                        n_estimators=1000, 
                        learning_rate = 0.01, 
                        # num_leaves = 32, 
                        
                        metric = 'mape')

gbm = joblib.load(f'./lgbm/{mode}all.pkl')

ReportPath = f"./final_inference"
checkAndMakeDir(ReportPath)
ReportName = f"lgbm_{mode}.csv"

# evaluate model
start_time= time.time()
pred = gbm.predict(test_Feat)
end_time = time.time()

test_Feat['prediction'] = pred
test_Feat['label'] = test_Price
total_inf += round(end_time - start_time, 5)
print("Total Seconds of one data: ", total_inf)
print(test_Feat.shape)
test_Feat.to_csv(f'./final_inference/{ReportName}')
