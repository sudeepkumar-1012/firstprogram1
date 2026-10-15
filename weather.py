from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Dashboard</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100vh;
            padding: 28px 16px;
            font-family: Arial, sans-serif;
            color: #172554;
            background: linear-gradient(135deg, #dbeafe, #eff6ff, #bfdbfe);
        }
        .container { width: 100%; max-width: 760px; margin: 24px auto; }
        h1 { text-align: center; margin-bottom: 8px; color: #1d4ed8; }
        .subtitle { text-align: center; color: #64748b; margin-bottom: 26px; }
        .panel {
            background: white;
            padding: 24px;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(30, 64, 175, .10);
            margin-bottom: 20px;
        }
        form { display: flex; gap: 10px; }
        input {
            flex: 1; min-width: 0; padding: 14px;
            border: 1px solid #cbd5e1; border-radius: 10px;
            font-size: 16px; outline-color: #2563eb;
        }
        button {
            border: 0; border-radius: 10px; padding: 14px 20px;
            background: #2563eb; color: white; font-size: 16px;
            font-weight: bold; cursor: pointer;
        }
        button:hover { background: #1d4ed8; }
        .error {
            padding: 14px; border-radius: 10px; margin-bottom: 20px;
            color: #991b1b; background: #fee2e2;
        }
        .location { text-align: center; color: #64748b; }
        .main-weather { text-align: center; padding: 18px 0; }
        .temperature { font-size: 64px; font-weight: bold; color: #2563eb; margin: 10px 0; }
        .condition { font-size: 21px; font-weight: bold; }
        .details {
            display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px; margin-top: 20px;
        }
        .detail { padding: 18px; background: #f1f5f9; border-radius: 12px; }
        .detail p { margin: 0 0 9px; color: #64748b; }
        .detail h3 { margin: 0; font-size: 20px; overflow-wrap: anywhere; }
        .footer { text-align: center; color: #64748b; font-size: 13px; margin-top: 22px; }
        a { color: #2563eb; }
        @media (max-width: 520px) {
            form { flex-direction: column; }
            button { width: 100%; }
            .temperature { font-size: 50px; }
            .details { grid-template-columns: 1fr; }
            .panel { padding: 18px; }
        }
    </style>
</head>
<body>
    <main class="container">
        <h1>🌦 Weather Dashboard</h1>
        <p class="subtitle">Check the current weather in any city</p>

        <section class="panel">
            <form method="POST">
                <input type="text" name="city" placeholder="Enter city, e.g. Bengaluru"
                       value="{{ city }}" aria-label="City name" required>
                <button type="submit">Get Weather</button>
            </form>
        </section>

        {% if error %}
            <div class="error" role="alert">{{ error }}</div>
        {% endif %}

        {% if weather %}
        <section class="panel">
            <p class="location">📍 {{ weather.city }}{% if weather.country %}, {{ weather.country }}{% endif %}</p>
            <div class="main-weather">
                <div class="temperature">{{ weather.temperature }}°C</div>
                <div class="condition">{{ weather.condition }}</div>
                <p>Feels like {{ weather.feels_like }}°C</p>
                <p>Today's range: {{ weather.min_temp }}°C – {{ weather.max_temp }}°C</p>
            </div>

            <div class="details">
                <div class="detail"><p>💧 Humidity</p><h3>{{ weather.humidity }}%</h3></div>
                <div class="detail"><p>💨 Wind speed</p><h3>{{ weather.wind_speed }} km/h</h3></div>
                <div class="detail">
                    <p>🌧 Chance of rain today</p>
                    <h3>{% if weather.rain_chance is not none %}{{ weather.rain_chance }}%{% else %}Unavailable{% endif %}</h3>
                </div>
                <div class="detail"><p>🌦 Current precipitation</p><h3>{{ weather.precipitation }} mm</h3></div>
                <div class="detail"><p>🌅 Sunrise</p><h3>{{ weather.sunrise }}</h3></div>
                <div class="detail"><p>🌇 Sunset</p><h3>{{ weather.sunset }}</h3></div>
            </div>
            <p class="footer">Weather observation time: {{ weather.updated_at }}</p>
        </section>
        {% endif %}

        <p class="footer">Weather data provided by <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a></p>
    </main>
</body>
</html>
"""


def get_weather(city):
    """Return a weather report for a city, or (None, error_message)."""
    geo_response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    geo_response.raise_for_status()
    locations = geo_response.json().get("results", [])

    if not locations:
        return None, "City not found. Please check the spelling and try again."

    location = locations[0]
    weather_response = requests.get(
        WEATHER_URL,
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": (
                "temperature_2m,relative_humidity_2m,apparent_temperature,"
                "precipitation,weather_code,wind_speed_10m"
            ),
            "daily": (
                "temperature_2m_max,temperature_2m_min,"
                "precipitation_probability_max,sunrise,sunset"
            ),
            "timezone": "auto",
            "forecast_days": 1,
        },
        timeout=10,
    )
    weather_response.raise_for_status()

    data = weather_response.json()
    current = data["current"]
    daily = data["daily"]

    report = {
        "city": location["name"],
        "country": location.get("country", ""),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "precipitation": current["precipitation"],
        "condition": WEATHER_CODES.get(current["weather_code"], "Unknown conditions"),
        "max_temp": daily["temperature_2m_max"][0],
        "min_temp": daily["temperature_2m_min"][0],
        "rain_chance": (
            daily["precipitation_probability_max"][0]
            if daily.get("precipitation_probability_max")
            else None
        ),
        "sunrise": daily["sunrise"][0].split("T")[-1],
        "sunset": daily["sunset"][0].split("T")[-1],
        "updated_at": current["time"].replace("T", " "),
    }
    return report, None


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            try:
                weather, error = get_weather(city)
            except requests.RequestException:
                error = "Could not connect to the weather service. Check your internet and try again."
            except (KeyError, IndexError, ValueError, TypeError):
                error = "Weather data is temporarily unavailable. Please try again."

    return render_template_string(HTML, weather=weather, error=error, city=city)


if __name__ == "__main__":
    app.run(debug=True)
