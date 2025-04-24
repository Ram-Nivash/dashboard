from flask import Flask, render_template, jsonify
from sensor_data import generate_dummy_data

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(generate_dummy_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)