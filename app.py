import blob_azure_demo as func
import json
import random

app = func.FunctionApp()

WIND_DATA = [
    {"station": "Vlissingen", "wind_dir": 220},
    {"station": "Leeuwarden", "wind_dir": 270},
    {"station": "Lelystad", "wind_dir": 250},
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