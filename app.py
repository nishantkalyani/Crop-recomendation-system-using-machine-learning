from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Function to fetch temperature from OpenWeatherMap API
def get_temperature(lat, lon):
    api_key = 'bd2cda27aaeafe15c4114ca562343e23'  # Your OpenWeatherMap API key
    base_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        return temperature
    else:
        return None

# Dummy crop recommendation function (you should implement your own logic)
def recommend_crop(nitrogen, phosphorus, potassium, humidity, rainfall, temperature):
    # Placeholder recommendation logic based on simple conditions
    if temperature > 30:
        return "Rice"
    elif temperature > 20:
        return "Wheat"
    elif humidity > 60 and rainfall > 100:
        return "Sugarcane"
    else:
        return "Maize"

@app.route('/temperature', methods=['POST'])
def temperature():
    lat = request.form.get('Latitude')
    lon = request.form.get('Longitude')
    temp = get_temperature(lat, lon)
    if temp is not None:
        return jsonify({"temperature": temp})
    else:
        return jsonify({"error": "Unable to fetch temperature"}), 404

@app.route('/predict', methods=['POST'])
def predict():
    nitrogen = float(request.form.get('Nitrogen'))
    phosphorus = float(request.form.get('Phosporus'))
    potassium = float(request.form.get('Potassium'))
    humidity = float(request.form.get('Humidity'))
    rainfall = float(request.form.get('Rainfall'))
    lat = request.form.get('Latitude')
    lon = request.form.get('Longitude')

    # Get temperature
    temperature = get_temperature(lat, lon)

    # Get crop recommendation based on inputs
    crop = recommend_crop(nitrogen, phosphorus, potassium, humidity, rainfall, temperature)

    return render_template('index.html', result=crop, temperature=temperature)

@app.route('/')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
