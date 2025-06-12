# app.py
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Fixed pickle loading - use binary mode
with open('house_price_prediction.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if model is fitted
        if not hasattr(model, 'coef_'):
            return render_template('index.html',prediction_text="Error: Model not trained. Please contact administrator.")
        features = [
            float(request.form['CRIM']),
            float(request.form['ZN']),
            float(request.form['INDUS']),
            float(request.form['CHAS']),
            float(request.form['NOX']),
            float(request.form['RM']),
            float(request.form['AGE']),
            float(request.form['DIS']),
            float(request.form['RAD']),
            float(request.form['TAX']),
            float(request.form['PTRATIO']),  # Fixed typo from PTRAIIO
            float(request.form['B']),
            float(request.form['LSTAT'])
        ]
        features_array = np.array([features])
        prediction = model.predict(features_array)
        price_in_dollars = prediction[0] * 1000  # Convert from thousands to dollars
        output = round(price_in_dollars, 2)
        return render_template('index.html', prediction_text=f"Predicted price: ${output:,.2f}")
    except Exception as e:
        error = f"Error: {str(e)}. Please check your inputs."
        return render_template('index.html', prediction_text=error)

if __name__ == "__main__":
    app.run(debug=True)