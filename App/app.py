from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import sklearn
import json

app = Flask(__name__)

# Load your model
ML_MODEL = joblib.load("models/target_large")
EXPECTED_COLUMNS = [
    'year', 'make', 'model', 'body', 'trim', 'mileage', 'newTireCount',
    'exteriorColor', 'interiorColor', 'transmission', 'driveTrain',
    'mpgCity', 'mpgHighway', 'cylinders', 'horsepower', 'horsepowerRpm',
    'engineSize', 'engineTorque', 'engineTorqueRpm']
CATEGORICAL_COLUMNS = ['make', 'model', 'body', 'trim', 'exteriorColor', 
                    'interiorColor', 'transmission', 'driveTrain']
NUMERICAL_COLUMNS = ['year', 'mileage', 'newTireCount',
    'mpgCity', 'mpgHighway', 'cylinders', 'horsepower', 'horsepowerRpm',
    'engineSize', 'engineTorque', 'engineTorqueRpm']

target_encodings = json.load(open('DATA/target_values.json', 'r'))
categorical_options = json.load(open('DATA/categorical_options.json', 'r'))
numerical_values = NUMERICAL_COLUMNS.copy()

@app.route('/')
def home():
    return render_template('index.html', categorical_input = categorical_options, numerical_input = numerical_values)


@app.route('/predict', methods=['POST'])
def predict():
    template = pd.DataFrame(columns=EXPECTED_COLUMNS, index=[0])
    user_input = request.form.to_dict()
    print(request.form)
    print(user_input)
   
    for col in CATEGORICAL_COLUMNS:
        if col in user_input:
            # convert to target encodings
            template[col] = target_encodings[col].get(user_input[col], np.nan)
    
    for col in NUMERICAL_COLUMNS:
        if col in user_input:
            template[col] = pd.to_numeric(user_input[col])
    
    # input_template = input_template.fillna({
    #     'year': df_train['year'].median(),
    #     'mileage': df_train['mileage'].median(),
    # })

    prediction = ML_MODEL.predict(template)[0]
    return jsonify({'prediction': f'${prediction:,.2f}'})
if __name__ == '__main__':
    app.run(debug=True)
