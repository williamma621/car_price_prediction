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
TARGET_ENCODINGS = json.load(open('DATA/target_values.json', 'r'))

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
   
    for col in CATEGORICAL_COLUMNS:  # Your categorical columns
        if col in user_input:
            # Use your pre-calculated target encodings
            template[col] = TARGET_ENCODINGS[col].get(user_input[col], np.nan)
    
    # 5. Fill numerical fields
    for col in NUMERICAL_COLUMNS:  # ['year', 'mileage', etc.]
        if col in user_input:
            template[col] = pd.to_numeric(user_input[col])
    
    # 6. Handle missing values (example: fill with median)
    # input_template = input_template.fillna({
    #     'year': df_train['year'].median(),
    #     'mileage': df_train['mileage'].median(),
    #     # Add other columns as needed
    # })

    prediction = ML_MODEL.predict(template)[0]
    return jsonify({'prediction': f'${prediction:,.2f}'})
if __name__ == '__main__':
    app.run(debug=True)