import azure.functions as func
from .cosmos_db_utils import insert_data_into_cosmos_db

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Define your Cosmos DB account and database details
    cosmos_db_endpoint = "your_cosmos_db_endpoint"
    cosmos_db_key = "your_cosmos_db_key"
    database_id = "your_database_id"
    container_id = "your_container_id"

    # Define the data to be inserted
    data = {
        "id": "119",
        "patient_id": "123",
        "zip_code": "110094",
        "radius_zip_code": "8",
        "provider_id": "367",
        "appointment_slot_id": "2",
        "appointment_id": "63",
        "provider_name": "peter smith",
        "appointment_status": "confirmed",
        "appointment_type": "general checkup",
        "appointment_date": "89/17/2023",
        "appointment_time": "4:58 PM",
        "app_booking": "true"
    }

    # Call the function to insert data into Cosmos DB
    insert_data_into_cosmos_db(cosmos_db_endpoint, cosmos_db_key, database_id, container_id, data)

    return func.HttpResponse("Data inserted successfully.")
