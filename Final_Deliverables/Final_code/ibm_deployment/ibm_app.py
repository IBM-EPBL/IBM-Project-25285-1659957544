import os
import numpy as np 
from flask import Flask,request,render_template 
import pickle
import requests
API_KEY = "GNwS1j0hd0M1Qx01hsyioQrviGjjB-oCzfNKRMwtt72D"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app= Flask(__name__)
@app.route('/')
def home():
    return render_template("web.html")
@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/info')
def info():
    return render_template("info.html")
@app.route('/login' ,methods = ['POST'])
def login(): 
    if request.method=='POST':
        do = float(request.form['do'])
        ph = float(request.form['ph'])
        co = float(request.form['co'])
        bod = float(request.form['bod'])
        na = float(request.form['na'])
        tc = float(request.form['tc'])
        X = [[do,ph,co,bod,na,tc]]
        payload_scoring = {"input_data": 
			[{"field": [["do", "ph","co","bod","na","tc"]], 
                "values": X}]}
        print(payload_scoring)
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/14bbb122-5f65-4ed1-9b14-01232a0cc439/predictions?version=2022-11-17', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        predictions =response_scoring.json()
        print(predictions)
        print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])
        pred =response_scoring.json()
        output = pred['predictions'][0]['values'][0][0]
        print(output)
        return render_template("web.html",showcase ='The WQI predicted is '+str(output))
    else:
        return render_template("web.html",predictions="Please check the values")
if __name__=="__main__":
    app.run(debug=False,port=5000)