from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  # Add this for cross-origin requests
import joblib
import warnings
from sklearn.exceptions import DataConversionWarning, UndefinedMetricWarning

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DataConversionWarning)
app = Flask(__name__)
CORS(app)  # Enable CORS to accept requests from Raspberry Pi

# Load pre-trained models (ensure these files are in the same directory as app.py)
try:
    isolation_model = joblib.load(open('isolation_forest_model.pkl', 'rb'))
    random_forest_model =joblib.load(open('random_forest_co2_model.pkl', 'rb'))
    print("Isolation Forest Model loaded successfully!")
    print("Random Forest Model loaded successfully!")
except Exception as e:
    print("Error loading model files:", e)
    isolation_model = None
    random_forest_model = None

# Global variable to store latest sensor data
sensor_data = {
    'temperature': None,
    'humidity': None,
    'co2': None,
    'air_quality': '--',
    'timestamp': '--',
    'anomaly': False,
    'forecast': None
}

co2_history = [350, 330, 320]

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(sensor_data)

@app.route('/update', methods=['POST'])

def update_data():
    global sensor_data, co2_history
    try:
        data = request.json
        # Calculate air quality based on CO2 levels
        temperature = float(data.get('temperature', 0.0))
        humidity = float(data.get('humidity', 0.0))
        # co2 = float(data.get('co2', 0.0))
        co2 = data.get('ppm', 0)
        if co2 < 1000:
            air_quality = 'Good'
        elif 1000 <= co2 < 2000:
            air_quality = 'Fair'
        elif 2000 <= co2 < 5000:
            air_quality = 'Moderate'
        else:
            air_quality = 'Poor'

        # Update CO2 history (keep only last 100 entries to limit memory)
        co2_history.append(co2)
        if len(co2_history) > 100:
            co2_history.pop(0)


     # Anomaly detection using Isolation Forest
        anomaly = False
        if isolation_model is not None:
            prediction = isolation_model.predict([[co2]])
            if prediction[0] == -1:
                anomaly = True

        # Forecast next CO2 using Random Forest (using last 3 CO2 readings)
        forecast_value = None
        if random_forest_model is not None and len(co2_history) >= 3:
            last_three = co2_history[-3:]
            print("Last 3 CO₂ values used for forecasting:", last_three)  # Debug line
            forecast_value = float(random_forest_model.predict([last_three])[0])
        print("Forecasted CO₂:", forecast_value)

        # Update the latest sensor data dictionary
        sensor_data = {
            'temperature': round(data.get('temperature', 0), 2),
            'humidity': round(data.get('humidity', 0), 2),
            'co2': int(co2),
            'air_quality': air_quality,
            'anomaly': anomaly,
            'forecast': round(forecast_value, 2) if forecast_value is not None else None
            # 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print("Error updating data:", e)
        return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
