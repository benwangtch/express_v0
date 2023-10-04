from flask import Flask, render_template, request
import json
import ast
import pandas as pd
from utils import *
from selectProperties import *
from featureImputation import *
from inference import *

app = Flask(__name__)

@app.route("/")
def hello(): 
	return render_template('index.html')


@app.route('/process/<data>', methods=['POST'])
def process(data):
    """The api used to get input from user, run all the algorithms and 
    output the five similar data and prediction.

    Args:
        data (json): The original input from users.

    Returns:
        output: A json format with two keys, groupData and output.
    """
    inputData = ast.literal_eval(data)
    api = []
    try:
        f = open('apiKey.txt')
        for line in f.readlines():
            api.append(line)
    except:
        print('ERROR: API key file might be missing.')
    # Convert from TWD97 to LatLon
    
    inputData = getLatLong(inputData, api) 
    
    # Demo Version: Read similar data from ./demo/, five similar datas are provided for each property type.
    if inputData['type'] == 'building':
        groupData = pd.read_csv('./demo/building_demo.csv', index_col=None)
    elif inputData['type'] == 'apartment':
        groupData = pd.read_csv('./demo/apartment_demo.csv', index_col=None)
    else:
        groupData = pd.read_csv('./demo/house_demo.csv', index_col=None)
    
    inferenceData = imputeMissingValues(inputData, groupData)
    
    output = inference(inputData['type'], inferenceData, inputData)
    # Get LatLon and addr for groupData to show on map
    groupData = getGroupLatLon(groupData, api)
    groupData = groupData.to_json()

    output={'groupData':groupData,'output':output }
    print('Inference done.')
    return output

if __name__=='__main__':
    app.run(debug=True)