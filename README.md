# 30 Days Devops Challenge - Weather Dashboard

## Weather Data Collection System - DevOps Day 1 Challenge
The Weather Dashboard is a Python application that fetches weather data for a specified city using the OpenWeather API and saves the data to an AWS S3 bucket.

## Features

- Fetch real-time weather data for a city from the OpenWeather API
- Displays temperature (°C), humidity, and other   weather conditions
- Save weather data to an AWS S3 bucket
- Search for cities from a predefined list
- Timestamps data for historical tracking

## Prerequisites

- Python 3.7+
- AWS account with S3 access
- OpenWeather API key

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/davebryan001/weather-dashboard.git
    cd weather-dashboard
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    path\\to\\env\\Scripts\\activate  # On Windows
    source venv/bin/activate      # On macOS/Linux
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a .env file in the root directory and add your OpenWeather API key and AWS S3 bucket name:
    ```env
    OPENWEATHER_API_KEY=your_openweather_api_key
    AWS_BUCKET_NAME=your_s3_bucket_name
    ```

## Usage

1. Run the application:
    ```sh
    python src/weather-dashboard.py
    ```

2. Follow the prompts to search for a city and fetch its weather data.

## Project Structure
weather-dashboard/
  src/
    __init__.py
    weather_dashboard.py
  tests/
  data/
    cities.json
  .env
  .gitignore
  requirements.txt
  README.md

## What I Learned

During the development of this project, I learned:

- How to interact with the OpenWeather API to fetch weather data.
- How to handle user input and validate choices in a command-line application.
- How to use AWS S3 to store and retrieve data using the AWS python sdk.
- Error handling in distributed systems.


