from flask import Flask, jsonify, request
import random

app = Flask(__name__)

stations = {
    "vlissingen": "Vlissingen",
    "schiphol": "Schiphol",
    "debilt": "De Bilt",
    "eelde": "Eelde",
    "maastricht": "Maastricht",
    "leeuwarden": "Leeuwarden",
    "rotterdam": "Rotterdam"
}

@app.route("/")
def home():
    return "Wind API is running"


@app.route("/api/wind")
def get_wind():
    station_key = request.args.get("station", "vlissingen").lower()

    if station_key not in stations:
        return jsonify({
            "error": "Invalid station",
            "available_stations": list(stations.keys())
        }), 400

    wind_speed = round(random.uniform(0, 15), 1)

    return jsonify({
        "station": stations[station_key],
        "wind_speed": wind_speed,
        "unit": "m/s"
    })


if __name__ == "__main__":
    app.run(debug=True)