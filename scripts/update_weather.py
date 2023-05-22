import requests
import os

API_KEY = os.getenv('WEATHER_API_KEY')
CITY = "London,uk"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

def weather_emoji(weather):
    if 'rain' in weather:
        return '🌧️'
    elif 'cloud' in weather:
        return '☁️'
    elif 'sunny' in weather or 'clear' in weather:
        return '☀️'
    elif 'snow' in weather:
        return '❄️'
    else:
        return ''

def temp_emoji(temp):
    if temp < 10:
        return '🧥'
    elif temp < 20:
        return '👕'
    else:
        return '🥶'

def fetch_weather():
    response = requests.get(API_URL)
    data = response.json()
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    temp = temp - 273.15  # Convert from Kelvin to Celsius
    return weather, temp

def update_readme(weather, temp):
    with open('README.md', 'r') as file:
        readme = file.read()

    weather_icon = weather_emoji(weather.lower())
    temp_icon = temp_emoji(temp)

    lines = readme.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('### working conditions..'):
            lines[i] = f'## working conditions..\n\nweather: {weather} {weather_icon}\n\ntemp: {temp:.2f} °C {temp_icon}'
            break
    else:
        lines.append(f'## working conditions..\n\nweather: {weather} {weather_icon}\n\ntemp: {temp:.2f} °C {temp_icon}')

    with open('README.md', 'w') as file:
        file.write('\n'.join(lines))

def main():
    weather, temp = fetch_weather()
    update_readme(weather, temp)

if __name__ == "__main__":
    main()
