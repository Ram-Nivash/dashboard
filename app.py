from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  # Add this for cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS to accept requests from Raspberry Pi

# Global variable to store latest sensor data
sensor_data = {
    'temperature': None,
    'humidity': None,
    'co2': None,
    'air_quality': '--',
    'timestamp': '--'
}

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(sensor_data)

@app.route('/update', methods=['POST'])
def update_data():
    global sensor_data
    try:
        data = request.json
        # Calculate air quality based on CO2 levels
        co2 = data.get('ppm', 0)
        if co2 < 1000:
            air_quality = 'Good'
        elif 1000 <= co2 < 2000:
            air_quality = 'Fair'
        elif 2000 <= co2 < 5000:
            air_quality = 'Moderate'
        else:
            air_quality = 'Poor'

        sensor_data = {
            'temperature': round(data.get('temperature', 0), 2),
            'humidity': round(data.get('humidity', 0), 2),
            'co2': int(co2),
            'air_quality': air_quality,
            # 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print("Error updating data:", e)
        return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)