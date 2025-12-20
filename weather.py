import os
import requests
from flask import Flask, jsonify, request


class Weather:
    DEFAULT_LOCATION = ("Sutton", "Quebec", "Canada")
    GEOCODE_URL = "https://api.openweathermap.org/geo/1.0/direct"
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("OPENWEATHER_API_KEY") or "29496e4dee3816490d136a80ac85f63d"

    def get_coordinates(self, location_tuple, api_key: str | None = None):
        api_key = api_key or self.api_key
        q = ",".join(location_tuple)
        params = {"q": q, "limit": 1, "appid": api_key}
        resp = requests.get(self.GEOCODE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            raise ValueError(f"No geocoding results for {q}")
        return float(data[0]["lat"]), float(data[0]["lon"])

    def get_current_weather(self, lat, lon, api_key: str | None = None, units="metric", lang="en"):
        api_key = api_key or self.api_key
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": units, "lang": lang}
        resp = requests.get(self.WEATHER_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_weather_for_location(self, location_tuple=None, units="metric", lang="en"):
        location_tuple = location_tuple or self.DEFAULT_LOCATION
        lat, lon = self.get_coordinates(location_tuple)
        return self.get_current_weather(lat, lon, units=units, lang=lang)

    def create_app(self):
        app = Flask(__name__)

        @app.route("/weather")
        def weather_endpoint():
            units = request.args.get("units", "metric")
            lang = request.args.get("lang", "en")
            city = request.args.get("city")
            state = request.args.get("state")
            country = request.args.get("country")

            if city and country:
                location = (city, state or "", country)
            else:
                location = self.DEFAULT_LOCATION

            try:
                lat, lon = self.get_coordinates(location)
                weather = self.get_current_weather(lat, lon, units=units, lang=lang)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

            result = {
                "location": {
                    "query": ",".join([p for p in location if p]),
                    "lat": lat,
                    "lon": lon,
                },
                "weather": {"raw": weather},
            }
            return jsonify(result)

        return app


if __name__ == "__main__":
    w = Weather()
    try:
        lat, lon = w.get_coordinates(Weather.DEFAULT_LOCATION)
        weather = w.get_current_weather(lat, lon, units="metric")
        main = weather.get("weather", [{}])[0]
        temp = weather.get("main", {}).get("temp")
        humidity = weather.get("main", {}).get("humidity")
        wind = weather.get("wind", {}).get("speed")
        desc = main.get("description")
        print(f"Location: {', '.join(Weather.DEFAULT_LOCATION)}")
        print(f"Coordinates: {lat}, {lon}")
        print(f"Weather: {desc}, temp={temp} °C, humidity={humidity}%, wind={wind} m/s")
    except Exception as e:
        print("Error fetching weather:", e)