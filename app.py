from flask import Flask, render_template, request
import json
import ast
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
    
    groupData = getSimilarProperties(inputData)
    # For Case study
    groupData.to_csv('./similar_data.csv', index=False) 
    inferenceData = imputeMissingValues(inputData, groupData)
    
    # For Case study
    outputInf = pd.DataFrame(inferenceData) 
    outputInf.to_csv('./inference_data.csv', index=False) 
    output = inference(inputData['type'], inferenceData, inputData)
    # Get LatLon and addr for groupData to show on map
    groupData = getGroupLatLon(groupData, api)
    groupData = groupData.to_json()

    output={'groupData':groupData,'output':output }
    print('Inference done.')
    return output

if __name__=='__main__':
    app.run(debug=True)