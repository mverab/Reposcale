# Notes API

Clean REST API for note management.

## Run locally
```
pip install -r requirements.txt
python src/app.py
```

## Docker
```
docker build -t notes-api .
docker run -p 5000:5000 notes-api
```

## Tests
```
pytest tests/
```
