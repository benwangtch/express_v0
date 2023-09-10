from flask import Flask, render_template, request
import json
import ast
from utils import *

app = Flask(__name__)

# Choose the model to use, return 1 for knn, 2 for Regram, 3 for LGBM
def switcher(data):
    city = data['addr'][0:3]
    type = data['type']
    for idx,item in enumerate(CityList):
        if city == item:
            if type == 'building':
                return BuildingModel[idx]
            elif type == 'apartment':
                return ApartmentModel[idx]
            else:
                return HouseModel[idx]
            
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
    # data = json.loads('data')
    data = ast.literal_eval(data)
    print(data)
    # process the data using Python code
    return data

if __name__=='__main__':
    app.run(debug=True)