import random
from datetime import datetime

def generate_dummy_data():
    return {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'temperature': round(random.uniform(20, 35), 2),
        'humidity': round(random.uniform(30, 80)),
        'co2': random.randint(300, 2000),
        'air_quality': random.choice(['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor'])
    }