"""Weather CLI — only OpenWeatherMap provider implemented."""

import sys


def fetch_weather(city: str, api_key: str) -> dict:
    """Fetch weather from OpenWeatherMap only."""
    import httpx
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    resp = httpx.get(url)
    resp.raise_for_status()
    data = resp.json()
    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
    }


def display(weather: dict):
    """Plain text output — no charts."""
    print(f"Weather in {weather['city']}:")
    print(f"  Temperature: {weather['temp']}°C")
    print(f"  Conditions: {weather['description']}")


def main():
    if len(sys.argv) < 3:
        print("Usage: weather.py <city> <api_key>")
        sys.exit(1)
    weather = fetch_weather(sys.argv[1], sys.argv[2])
    display(weather)


if __name__ == "__main__":
    main()
