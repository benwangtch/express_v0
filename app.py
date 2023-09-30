from flask import Flask, render_template, request
import json
import ast
from utils import *
from selectData import *
from reconstructFeatures import *
from inference import *

app = Flask(__name__)

@app.route("/")
def hello(): 
	return render_template('index.html')


@app.route('/process/<data>', methods=['POST'])
def process(data):
    inputData = ast.literal_eval(data)
    
    inputData = getLatLong(inputData) # Convert from TWD97 to LatLon
    
    groupData = getSimilarData(inputData)
    
    groupData.to_csv('./sample_group_0.csv', index=False) # For Case study
    
    inferenceData = fillMissingFeature(inputData, groupData)
    
    outputInf = pd.DataFrame(inferenceData) # For Case study
    outputInf.to_csv('./inference_sample_0.csv', index=False) # For Case study
    
    output = inference(inputData['type'], inferenceData, inputData)
    # Get LatLon and addr for groupData to show on map
    groupData = getGroupLatLon(groupData)
    groupData = groupData.to_json()

    output={'groupData':groupData,'output':output }
    print('Inference done')
    return output

if __name__=='__main__':
    app.run(debug=True)