import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            # Simpler creation for us-east-1
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_s3(self, weather_data, city):
        """Save weather data to S3 bucket"""
        if not weather_data:
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"
        
        try:
            weather_data['timestamp'] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {city} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False

    def load_cities(self):
        """Load available cities from JSON file"""
        try:
            # Open the file with UTF-8 encoding
            with open('data/cities.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Check if the JSON content is a list
                if isinstance(data, list):
                    return [city['name'] for city in data]  # Extract just the city names
                else:
                    print("Error: Expected a list of cities in cities.json.")
                    return []
        except FileNotFoundError:
            print("Error: cities.json file not found!")
            return []
        except UnicodeDecodeError as e:
            print(f"Error decoding the JSON file: {e}")
            return []




def search_cities(cities, query, limit=15):
    """Search cities by a query and return a limited number of results"""
    # Filter cities case-insensitively
    filtered_cities = [city for city in cities if query.lower() in city.lower()]
    return filtered_cities[:limit]
   
def main():
    dashboard = WeatherDashboard()
    
    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()
    
    cities = dashboard.load_cities()
    
    if not cities:
        print("No cities available for search.")
        return
    
    # get user input
    query = input("Enter a city's name to search: ")
    
    # search json for city name
    search_results = search_cities(cities, query)
    
    if not search_results:
        print(f"No cities found matching '{query}'. Try a different search.")
        return

    print(f"\nSearch results for '{query}':")
    for index, city in enumerate(search_results, start=1):
        print(f"{index}. {city}")
    
    try:
        # ask user to input a number corresponding to a city
        choice = int(input("\nEnter the number of the city you want to search for: ")) - 1
        
        if choice < 0 or choice >= len(search_results):
            print("Invalid choice!")
            return
        
        city = search_results[choice]
        print(f"\nYou selected: {city}")
        
        # get the weather for selected city
        weather_data = dashboard.fetch_weather(city)
        
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temp}°C")
            print(f"Feels like: {feels_like}°C")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            
            # Save weather data to S3
            dashboard.save_to_s3(weather_data, city)
        else:
            print(f"Failed to fetch weather data for {city}")
        
    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
