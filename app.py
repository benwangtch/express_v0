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
    # inputData = getLatLong(data) 
    inputData = {'type':'house','x座標':169784.98804265473,'y座標':2543493.999829864, 'age':33, 'far':1.58,'trans1':3.024 }
    # process the data using Python code
    groupData = getSimilarData(inputData)
    inferenceData = fillMissingFeature(inputData, groupData)
    output = inference(inputData['type'], inferenceData)
    # print("The output price is: ", output['預測價格'])
    print(output)
    return output

if __name__=='__main__':
    app.run(debug=True)