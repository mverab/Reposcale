# WeatherCLI

A powerful weather CLI with multiple providers, caching, and chart output.

## Features
- **Multi-provider**: OpenWeatherMap, WeatherAPI, and AccuWeather
- **Local caching**: SQLite-based cache to reduce API calls
- **Chart output**: Beautiful terminal charts with sparklines
- **Offline mode**: Use cached data when no internet available

## Usage
```bash
python src/weather.py <city> <api_key> [--provider owm|wapi|accu] [--chart]
```

## Configuration
See `docs/configuration.md` for provider setup and cache options.
