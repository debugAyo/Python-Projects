import requests

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]
        wind = data.get('wind', {})

        temp = main.get('temp')
        humidity = main.get('humidity')
        pressure = main.get('pressure')
        description = weather.get('description')
        wind_speed = wind.get('speed')

        print(f"\nWeather in {city.capitalize()}:")
        print(f"Temperature: {temp}°C")
        print(f"Description: {description.capitalize()}")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        print("Error: City not found. Please check your spelling.")

def main():
    print("Program started!")  # 👈 For debugging
    api_key = "c9576e70cd97e1a05bb8ef9215fd849e"
    city = input("Enter your city name: ")
    get_weather(city, api_key)

if __name__ == "__main__":
    main()
