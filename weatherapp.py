from flask import Flask, render_template, request
import requests

app = Flask(__name__)
OPENWEATHERMAP_API_KEY = "replace with your own api key"
OPENWEATHERMAP_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
    return render_template('index.html', weather_data=weather_data)

def get_weather(city):
    params = {
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(OPENWEATHERMAP_URL, params=params)
    print("API Response Status Code:", response.status_code)  # Debugging
    print("API Response Text:", response.text)  # Debugging
    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'background': get_background(data['weather'][0]['description'])  # Add background based on weather condition
        }
        return weather
    else:
        return None
def get_background(weather_description):
    backgrounds = {
        'clear sky': 'linear-gradient(135deg, #ff7e5f, #feb47b)',  # Sunny gradient
        'rain': 'linear-gradient(135deg, #2c3e50, #3498db)',  # Rainy gradient
        'clouds': 'linear-gradient(135deg, #bdc3c7, #2c3e50)',  # Cloudy gradient
        'snow': 'linear-gradient(135deg, #ffffff, #bdc3c7)',  # Snowy gradient
        # Add more weather conditions and backgrounds as needed
    }
    # Default background if weather condition is not in the mapping
    return backgrounds.get(weather_description.lower(), 'linear-gradient(135deg, #6a11cb, #2575fc)')
if __name__ == '__main__':
    app.run(debug=True)