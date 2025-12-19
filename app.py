import os
import requests
from flask import Flask, jsonify, request

# Default location: Longueuil, Quebec, Canada
DEFAULT_LOCATION = ("Longueuil", "Quebec", "Canada")

# API key: prefer environment variable, fall back to the key present earlier
API_KEY = os.environ.get("OPENWEATHER_API_KEY") or "442cbef5bb5cae228df065d62e7475cd"

GEOCODE_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_coordinates(location_tuple, api_key=API_KEY):
    """Return (lat, lon) for a given (city, state, country) tuple using OWM geocoding."""
    q = ",".join(location_tuple)
    params = {"q": q, "limit": 1, "appid": api_key}
    resp = requests.get(GEOCODE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ValueError(f"No geocoding results for {q}")
    return float(data[0]["lat"]), float(data[0]["lon"])

def get_current_weather(lat, lon, api_key=API_KEY, units="metric", lang="en"):
    """Return current weather JSON from OpenWeatherMap for given coordinates."""
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": units, "lang": lang}
    resp = requests.get(WEATHER_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

app = Flask(__name__)


@app.route("/weather")
def weather_endpoint():
    """HTTP endpoint: returns weather for Longueuil by default.
    Optional query params: units (metric|imperial), lang (en|fr), city,state,country
    """
    units = request.args.get("units", "metric")
    lang = request.args.get("lang", "en")
    city = request.args.get("city")
    state = request.args.get("state")
    country = request.args.get("country")

    if city and country:
        location = (city, state or "", country)
    else:
        location = DEFAULT_LOCATION

    try:
        lat, lon = get_coordinates(location)
        weather = get_current_weather(lat, lon, units=units, lang=lang)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    result = {
        "location": {
            "query": ",".join([p for p in location if p]),
            "lat": lat,
            "lon": lon,
        },
        "weather": {
            "raw": weather,
        },
    }
    return jsonify(result)


if __name__ == "__main__":
    # When run as a script, fetch and print a friendly summary for Longueuil
    try:
        lat, lon = get_coordinates(DEFAULT_LOCATION)
        weather = get_current_weather(lat, lon, units="metric")
        main = weather.get("weather", [{}])[0]
        temp = weather.get("main", {}).get("temp")
        humidity = weather.get("main", {}).get("humidity")
        wind = weather.get("wind", {}).get("speed")
        desc = main.get("description")
        print(f"Location: {', '.join(DEFAULT_LOCATION)}")
        print(f"Coordinates: {lat}, {lon}")
        print(f"Weather: {desc}, temp={temp} °C, humidity={humidity}%, wind={wind} m/s")
    except Exception as e:
        print("Error fetching weather:", e)