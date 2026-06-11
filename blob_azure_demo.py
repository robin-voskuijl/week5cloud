from flask import Flask, jsonify, request
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Wind API is running"

@app.route("/api/wind")
def get_wind():
    station = request.args.get("station", "Vlissingen")

    wind_speed = round(random.uniform(0, 15), 1)

    return jsonify({
        "station": station,
        "wind_speed": wind_speed,
        "unit": "m/s",
        "message": f"Wind data for {station}"
    })

if __name__ == "__main__":
    app.run()