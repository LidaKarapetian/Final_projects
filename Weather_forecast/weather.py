#!/usr/bin/python

"""
Weather forecast - the user should provide the name of the city 
and get the detailed weather information. 
He can also provide another option to get only the requested info: 
temperature, humidity, etc… he can also provide a list of details and get only those ones.
"""

import argparse
import subprocess
import importlib.util

def check_module_and_install(module_name):
    """
    This function checks if the module is installed.
    If not, it attempts to install the module using the 'pip' command.
    """
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        try:
            subprocess.run(["pip", "install", module_name], check=True)
            print(f"Successfully installed the '{module_name}' module.")
        except subprocess.CalledProcessError as error:
            print(f"Error installing the '{module_name}' module: {error}")
            return False
    return True

try:
    import requests
except ModuleNotFoundError:
    print("The 'requests' module isn't installed.")
    check_module_and_install("requests")
    import requests

def get_weather_forecast(city_name, api_key, unit_system, main_url):
    """
    This function fetches weather data for a specified city from the OpenWeather API.
    """
    parameters = {
        'appid': api_key,
        'q': city_name,
        'units': unit_system
    }
    response = requests.get(main_url, params=parameters, timeout=10)
    if response.status_code == 200:
        data = response.json() #type dict
        return data
    print("Error: Status code", response.status_code)
    return None

def display_weather(forecast_data, options, unit_system):
    """
    This function displays the weather details based on the user's specified options.
    """
    if forecast_data is not None:
        if unit_system == 'metric':
            if options.description:
                print(f"Description: {forecast_data['weather'][0]['description']}")        
            if options.temperature:
                print(f"Temperature: {forecast_data['main']['temp']}°C")
            if options.humidity:
                print(f"Humidity: {forecast_data['main']['humidity']}%")
            if options.visibility:
                print(f"Visibility: {forecast_data['visibility']}meter")
        elif unit_system == 'imperial':
            if options.description:
                print(f"Description: {forecast_data['weather'][0]['description']}")
            if options.temperature:
                print(f"Temperature: {forecast_data['main']['temp']}°F")
            if options.humidity:
                print(f"Humidity: {forecast_data['main']['humidity']}%")
            if options.visibility:
                print(f"Visibility: {forecast_data['visibility']}miles")
        elif unit_system == 'standard':
            if options.description:
                print(f"Description: {forecast_data['weather'][0]['description']}")
            if options.temperature:
                print(f"Temperature: {forecast_data['main']['temp']}K")
            if options.humidity:
                print(f"Humidity: {forecast_data['main']['humidity']}%")
            if options.visibility:
                print(f"Visibility: {forecast_data['visibility']}%")

def main():
    """
    Main function to handle the weather forecast display for a specified city.
    """
    main_url = 'http://api.openweathermap.org/data/2.5/weather'
    api_key = '73d2f95f17e382481555b7e1fb034c58'
 
    parser = argparse.ArgumentParser(description='Display weather forecast for a city.')
    parser.add_argument('city_name', type=str, nargs = '+', help='City to fetch weather data for')
    parser.add_argument('unit_system', type=str, help="Choose unit system: it can be metric, imperial or standard")
    parser.add_argument('--description', action='store_true', help='Show weather description')
    parser.add_argument('--temperature', action='store_true', help='Show temperature')
    parser.add_argument('--humidity', action='store_true', help='Show humidity')
    parser.add_argument('--visibility', action='store_true', help='Show visibility')

    args = parser.parse_args()
    city_name = args.city_name
    unit_system = args.unit_system
    
    data = get_weather_forecast(city_name, api_key, unit_system, main_url)
    if not any([args.description, args.temperature, args.humidity, args.visibility]):
        print(f"Weather forecast details: {city_name} ")
        args.description = args.temperature = args.humidity = args.visibility = True
        display_weather(data, args, unit_system)
        

if __name__ == "__main__":
    main()


