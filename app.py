from flask import Flask, render_template, request
import random
from datetime import datetime

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index1():
    return render_template('landing.html')

@app.route('/predict', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        date_input = request.form['date']
        region = request.form['region']
        
        # Extract month from date input
        date_obj = datetime.strptime(date_input, '%Y-%m-%d')
        month = date_obj.month
        
        # Determine "Rain" or "No Rain"
        if 7 <= month <= 10:  # Rainy season
            result = "Rain" if random.random() < 0.7 else "No Rain"
        else:  # Mostly dry season
            result = "Rain" if random.random() < 0.08 else "No Rain"

    return render_template('index.html', result=result)

@app.route('/flkj', methods=['POST'])
def predict_rain():
    data = request.json
    city = data['city']
    date = data['date']

    # Fetch current weather data for prediction features
    weather_response = requests.get(f'{BASE_URL}?key={API_KEY}&q={city}').json()
    
    if 'error' in weather_response:
        return jsonify({'error': 'City not found or invalid API call'}), 404

    temp = weather_response['current']['temp_c']
    humidity = weather_response['current']['humidity']
    wind_speed = weather_response['current']['wind_kph']
    pressure = weather_response['current']['pressure_mb']

    # Prepare data for model prediction
    input_data = np.array([[temp, humidity, wind_speed, pressure]])
    prediction = model.predict(input_data)

    result = 'rain' if prediction[0] == 1 else 'no rain'

    return jsonify({'city': city, 'date': date, 'prediction': result})

# if __name__ == '__main__':
#     app.run(debug=False,host='0.0.0.0')
