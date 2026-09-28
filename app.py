import requests
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)


# =====================================
# GET CITY COORDINATES
# =====================================

def get_coordinates(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    result = data["results"][0]

    return {
        "name": result.get("name", city),
        "country": result.get("country", ""),
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }


# =====================================
# GET WEATHER DATA
# =====================================

def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "daily": (
            "weather_code,"
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max"
        ),
        "timezone": "auto",
        "forecast_days": 7
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# =====================================
# WEATHER DESCRIPTION
# =====================================

def get_weather_description(code):

    weather_codes = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Overcast ☁️",
        45: "Foggy 🌫️",
        48: "Foggy 🌫️",
        51: "Light Drizzle 🌦️",
        53: "Drizzle 🌦️",
        55: "Heavy Drizzle 🌧️",
        61: "Light Rain 🌧️",
        63: "Moderate Rain 🌧️",
        65: "Heavy Rain 🌧️",
        71: "Light Snow ❄️",
        73: "Snow ❄️",
        75: "Heavy Snow ❄️",
        80: "Rain Shower 🌦️",
        81: "Rain Shower 🌧️",
        82: "Heavy Rain Shower ⛈️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with Hail ⛈️",
        99: "Heavy Thunderstorm ⛈️"
    }

    return weather_codes.get(
        code,
        "Unknown Weather"
    )


# =====================================
# DASHBOARD UI
# =====================================

st.title("🌤️ Weather Dashboard")

st.write(
    "Check current weather and 7-day forecast "
    "for any city."
)

st.divider()


city = st.text_input(
    "🏙️ Enter City Name",
    placeholder="Example: Delhi"
)


if st.button(
    "🔍 Get Weather",
    use_container_width=True
):

    if not city.strip():

        st.warning(
            "Please enter a city name."
        )

    else:

        try:

            with st.spinner(
                "Fetching weather data..."
            ):

                location = get_coordinates(
                    city.strip()
                )


                if location is None:

                    st.error(
                        "City not found."
                    )

                    st.stop()


                weather = get_weather(
                    location["latitude"],
                    location["longitude"]
                )


            current = weather["current"]


            st.success(
                "Weather data loaded successfully!"
            )


            st.header(
                f"📍 {location['name']}, "
                f"{location['country']}"
            )


            description = get_weather_description(
                current["weather_code"]
            )


            st.subheader(description)


            # CURRENT WEATHER CARDS

            col1, col2, col3, col4 = st.columns(4)


            col1.metric(
                "🌡️ Temperature",
                f"{current['temperature_2m']} °C"
            )


            col2.metric(
                "🤔 Feels Like",
                f"{current['apparent_temperature']} °C"
            )


            col3.metric(
                "💧 Humidity",
                f"{current['relative_humidity_2m']} %"
            )


            col4.metric(
                "💨 Wind Speed",
                f"{current['wind_speed_10m']} km/h"
            )


            st.divider()


            # =====================================
            # FORECAST TABLE
            # =====================================

            st.header("📅 7-Day Forecast")


            daily = weather["daily"]


            forecast_df = pd.DataFrame({

                "Date":
                    daily["time"],

                "Weather Code":
                    daily["weather_code"],

                "Max Temperature (°C)":
                    daily["temperature_2m_max"],

                "Min Temperature (°C)":
                    daily["temperature_2m_min"],

                "Rain Probability (%)":
                    daily[
                        "precipitation_probability_max"
                    ]
            })


            forecast_df["Date"] = pd.to_datetime(
                forecast_df["Date"]
            )


            forecast_df["Weather"] = (
                forecast_df["Weather Code"]
                .apply(get_weather_description)
            )


            display_df = forecast_df[
                [
                    "Date",
                    "Weather",
                    "Max Temperature (°C)",
                    "Min Temperature (°C)",
                    "Rain Probability (%)"
                ]
            ]


            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )


            # =====================================
            # TEMPERATURE CHART
            # =====================================

            st.header("📈 Temperature Forecast")


            temperature_data = (
                forecast_df
                .set_index("Date")
                [
                    [
                        "Max Temperature (°C)",
                        "Min Temperature (°C)"
                    ]
                ]
            )


            st.line_chart(
                temperature_data
            )


            # =====================================
            # RAIN CHART
            # =====================================

            st.header("🌧️ Rain Probability")


            rain_data = (
                forecast_df
                .set_index("Date")
                [
                    ["Rain Probability (%)"]
                ]
            )


            st.bar_chart(
                rain_data
            )


            # LOCATION DETAILS

            with st.expander(
                "📌 Location Details"
            ):

                st.write(
                    "Latitude:",
                    location["latitude"]
                )

                st.write(
                    "Longitude:",
                    location["longitude"]
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Internet connection error."
            )


        except requests.exceptions.Timeout:

            st.error(
                "Weather service timeout. Try again."
            )


        except requests.exceptions.RequestException as error:

            st.error(
                f"API Error: {error}"
            )


        except Exception as error:

            st.error(
                f"Error: {error}"
            )


st.divider()

st.caption(
    "Built with Python, Streamlit, Pandas and Open-Meteo API"
)