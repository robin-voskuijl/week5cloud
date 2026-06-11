from azure.storage.blob import BlobServiceClient
import uuid
import os
import azure.functions as func
import logging
import json

app = func.FunctionApp()

@app.blob_trigger(
    arg_name="myblob",
    path="wind-data/{name}",
    connection="AzureWebJobsStorage"
)
def process_wind_blob(myblob: func.InputStream):

    logging.info(f"Blob trigger fired: {myblob.name} ({myblob.length} bytes)")

    # Read the blob content
    content = myblob.read().decode("utf-8")

    # Parse it as JSON
    try:
        data = json.loads(content)
        logging.info(f"Station: {data.get('station')}, "
                     f"Wind speed: {data.get('wind_speed')} m/s")
    except json.JSONDecodeError:
        logging.warning("File was not valid JSON")

app = func.FunctionApp()

CONTAINER = "wind-data"

@app.route(route="save_wind", methods=["POST"])
def save_wind(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    conn_str = os.environ["AzureWebJobsStorage"]
    blob_service = BlobServiceClient.from_connection_string(conn_str)

    container_client = blob_service.get_container_client(CONTAINER)
    try:
        container_client.create_container()
    except Exception:
        pass

    blob_name = f"{uuid.uuid4()}.json"
    container_client.upload_blob(blob_name, json.dumps(body))

    return func.HttpResponse(
        json.dumps({"saved": blob_name}),
        mimetype="application/json",
        status_code=201
    )