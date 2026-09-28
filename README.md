# 🌦️ Weather Dashboard Using Python

A simple Weather Dashboard application developed using Python. The application allows users to enter a city name and get real-time weather information such as temperature, humidity, wind speed, and weather conditions using a weather API.

## 🚀 Features

* Search weather by city name
* Display current temperature
* Show humidity level
* Display wind speed
* Show current weather conditions
* Handle invalid city names
* Fetch real-time weather data
* Simple and easy-to-use interface

## 🛠️ Technologies Used

* Python
* Requests Library
* Weather API
* JSON Data Handling

## 📂 Project Structure

weather-dashboard/
│
├── weather.py
├── .env
├── requirements.txt
├── .gitignore
└── README.md

## ⚙️ Installation

### 1. Clone the Repository

git clone <your-repository-url>

cd weather-dashboard

### 2. Create a Virtual Environment

python -m venv venv

### 3. Activate the Virtual Environment

For Windows:

venv\Scripts\activate

For Linux/macOS:

source venv/bin/activate

### 4. Install Required Libraries

pip install -r requirements.txt

Or install the required packages manually:

pip install requests python-dotenv

## 🔑 API Key Setup

Create a `.env` file in the project folder and add your Weather API key:

WEATHER_API_KEY=your_api_key_here

Do not upload your `.env` file to a public repository.

Add the following to `.gitignore`:

.env
venv/
**pycache**/

## ▶️ Run the Application

Run the Python file using:

python weather.py

Enter the city name when prompted.

Example:

Enter city name: Chandigarh

Output:

City: Chandigarh
Temperature: 30°C
Weather: Clear Sky
Humidity: 55%
Wind Speed: 4.2 m/s

## 🔄 How It Works

1. The user enters a city name.
2. Python sends an HTTP request to the Weather API using the `requests` library.
3. The API returns weather data in JSON format.
4. Python processes the JSON response.
5. The application displays the weather details.

## 📦 Requirements

requests
python-dotenv

You can generate the `requirements.txt` file using:

pip freeze > requirements.txt

## 🔮 Future Improvements

* Add a graphical user interface using Tkinter
* Add a 5-day weather forecast
* Automatically detect the user's location
* Add Celsius and Fahrenheit conversion
* Save recent city searches
* Add weather icons
* Add better exception handling

## 👨‍💻 Author

Developed using Python as a beginner-friendly project to understand API integration, HTTP requests, JSON handling, environment variables, and exception handling.

## 📄 License

This project is created for educational and learning purposes.
