from flask import Flask, render_template, request
import json
import ast
from utils import *
from selectData import *
from reconstructFeatures import *
from inference import *

app = Flask(__name__)

            
def getSimiliarData():  
    pass
@app.route("/")
def hello(): 
	return render_template('index.html')


# @app.route('/', methods = ['POST', 'GET'])
# def data():
#     if request.method == 'GET':
#         return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#     if request.method == 'POST':
#         form_data = request.form
#         print(form_data)
#         return render_template('data.html',form_data = form_data)

@app.route('/process/<data>', methods=['POST'])
def process(data):
    data = ast.literal_eval(data)
    
    # Get (lat, long) by certain API's
    inputData = getLatLong(data) 
    
    # process the data using Python code
    groupData = getSimilarData(inputData)
    inferenceData = fillMissingFeature(inputData, groupData)
    
    ouputPrice = inference(inputData['type'], inferenceData)
    
    return data

if __name__=='__main__':
    app.run(debug=True)