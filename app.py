import numpy as np
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open('xgboost_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
@app.route('/',methods=['GET'])


def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])

def predict():
    
    if request.method == 'POST':
        
        cement = float(request.form['cement'])
        slag = float(request.form['slag'])
        flyash = float(request.form['flyash'])
        water = float(request.form['water'])
        superplasticizer = float(request.form['superplasticizer'])
        coarseaggregate = float(request.form['coarseaggregate'])
        fineaggregate = float(request.form['fineaggregate'])
        age = float(request.form['age'])
        
        X = [cement, slag, flyash, water, superplasticizer, coarseaggregate,
             fineaggregate, age]
        
        X = np.array(X)
        
        scaled = scaler.transform(X.reshape(1,-1))
        
        prediction = model.predict(scaled)
        
        output_num = round(prediction[0], 2)
        
        output = "{:.2f}".format(output_num)
        
        return render_template('result.html', pred = output)
                        
    else:
        
        return render_template('index.html')

if __name__=="__main__":
    
    app.run(debug=True)

