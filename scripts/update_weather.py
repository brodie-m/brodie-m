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
        readme = file.readlines()

    weather_icon = weather_emoji(weather.lower())
    temp_icon = temp_emoji(temp)

    new_content = f'### working conditions..\n\nweather: {weather} {weather_icon}\n\ntemp: {temp:.2f} °C {temp_icon}\n'
    start_marker = '<!--weather_start-->\n'
    end_marker = '<!--weather_end-->\n'
    
    if start_marker in readme and end_marker in readme:
        start = readme.index(start_marker) + 1
        end = readme.index(end_marker)
        readme[start:end] = new_content.split('\n')

    else:
        readme.append(start_marker + new_content + end_marker)

    with open('README.md', 'w') as file:
        file.write(''.join(readme))

def main():
    weather, temp = fetch_weather()
    update_readme(weather, temp)

if __name__ == "__main__":
    main()
