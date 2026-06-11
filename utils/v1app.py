import azure.functions as func
import json
import random

app = func.FunctionApp()

WIND_DATA = [
    {"station": "Vlissingen", "wind_speed": 7.4, "wind_dir": 220},
    {"station": "Leeuwarden", "wind_speed": 5.2, "wind_dir": 270},
    {"station": "Lelystad", "wind_speed": 4.9, "wind_dir": 250},
]

@app.route(route="wind", methods=["GET"])
def get_wind(req: func.HttpRequest) -> func.HttpResponse:

    station = req.params.get("station")

    data = []

    for item in WIND_DATA:
        item_copy = item.copy()
        item_copy["wind_speed"] = round(random.uniform(0, 15), 1)
        data.append(item_copy)

    if station:
        data = [d for d in data if d["station"] == station]

    return func.HttpResponse(
        json.dumps(data),
        mimetype="application/json",
        status_code=200
    )


@app.route(route="wind", methods=["POST"])
def add_wind(req: func.HttpRequest) -> func.HttpResponse:

    body = req.get_json()

    WIND_DATA.append({
        "station": body["station"],
        "wind_speed": body["wind_speed"],
        "wind_dir": body["wind_dir"]
    })

    return func.HttpResponse(
        json.dumps({"message": "Station added"}),
        mimetype="application/json",
        status_code=201
    )


@app.route(route="wind", methods=["PUT"])
def update_wind(req: func.HttpRequest) -> func.HttpResponse:

    body = req.get_json()

    for item in WIND_DATA:
        if item["station"] == body["station"]:
            item["wind_speed"] = body["wind_speed"]
            item["wind_dir"] = body["wind_dir"]

            return func.HttpResponse(
                json.dumps({"message": "Station updated"}),
                mimetype="application/json",
                status_code=200
            )

    return func.HttpResponse(
        json.dumps({"error": "Station not found"}),
        mimetype="application/json",
        status_code=404
    )

@app.route(route="wind", methods=["DELETE"])
def delete_wind(req: func.HttpRequest) -> func.HttpResponse:

    station = req.params.get("station")

    global WIND_DATA

    WIND_DATA = [
        item for item in WIND_DATA
        if item["station"] != station
    ]

    return func.HttpResponse(
        json.dumps({"message": "Station deleted"}),
        mimetype="application/json",
        status_code=200
    )