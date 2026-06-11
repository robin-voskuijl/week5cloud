# REST API using Flask (Proficient: data does not need to be persistent)
# Run locally with: python app.py
# Then visit: http://localhost:5000/api/wind or http://localhost:5000/api/wind?station=Vlissingen

from flask import Flask, jsonify, request
import random

app = Flask(__name__)

WIND_DATA = [
    {"station": "Vlissingen", "wind_dir": 220},
    {"station": "Leeuwarden", "wind_dir": 270},
    {"station": "Lelystad",   "wind_dir": 250},
]

@app.route("/")
def home():
    return "Wind API is running. Try /api/wind or /api/wind?station=Vlissingen"

@app.route("/api/wind")
def get_wind():
    station = request.args.get("station")

    data = []
    for item in WIND_DATA:
        item_copy = item.copy()
        item_copy["wind_speed"] = round(random.uniform(0, 15), 1)
        data.append(item_copy)

    if station:
        data = [d for d in data if d["station"] == station]

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
