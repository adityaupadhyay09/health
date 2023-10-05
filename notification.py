import os
import datetime
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
from pyfcm import FCMNotification
from pyapns2.client import APNsClient

# Azure credentials and configuration
subscription_id = 'your_subscription_id'
resource_group_name = 'your_resource_group'
cosmosdb_account_name = 'your_cosmosdb_account_name'
cosmosdb_database_name = 'your_cosmosdb_database_name'
cosmosdb_container_name = 'your_cosmosdb_container_name'

# Firebase Cloud Messaging (FCM) configuration
fcm_api_key = 'AAAAfj0tkGU:APA91bGrkD5Z_8FMTxMeO_K7M8LeMVmc7sHho-NHMjh5NMtSygK0n4aqOxY-R-cH63spNE-UtDE__w-I6VN9vs3mEwvEYl2w47530SVsYdMvlU5Zn6OZZr3MTkaFDdj9YOqBG122CvKM'  # Replace with your FCM API key

# Apple Push Notification Service (APNs) configuration
apns_cert_file = 'your_apns_cert.pem'  # Replace with the path to your APNs certificate file
apns_key_file = 'your_apns_key.pem'    # Replace with the path to your APNs key file

# Initialize Azure Cosmos DB client
credential = DefaultAzureCredential()
cosmos_client = CosmosClient(account_url=f'https://{cosmosdb_account_name}.documents.azure.com:443/',
                             credential=credential)

# Calculate notification schedule times
current_time = datetime.datetime.utcnow()
notification_72_hours = current_time + datetime.timedelta(hours=72)
notification_24_hours = current_time + datetime.timedelta(hours=24)

# Initialize FCM client
fcm_client = FCMNotification(api_key=fcm_api_key)

# Initialize APNs client
apns_client = APNsClient(credentials=(apns_cert_file, apns_key_file))

# Query Cosmos DB to get appointments
def get_appointments():
    appointments = []
    database = cosmos_client.get_database_client(cosmosdb_database_name)
    container = database.get_container_client(cosmosdb_container_name)
    query = f"SELECT * FROM c WHERE c.appointment_status = 'confirmed'"
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        appointment = {
            'appointment_id': item['appointment_id'],
            'patient_id': item['patient_id'],
            'appointment_date': item['appointment_date'],
            'appointment_time': item['appointment_time'],
            # Add more fields as needed
        }
        appointments.append(appointment)
    return appointments

# Get appointments from Cosmos DB
appointments = get_appointments()

# Send notifications
for appointment in appointments:
    appointment_id = appointment['appointment_id']
    patient_id = appointment['patient_id']
    appointment_date = appointment['appointment_date']
    appointment_time = appointment['appointment_time']

    appointment_datetime = datetime.datetime.strptime(f"{appointment_date} {appointment_time}", "%m/%d/%Y %I:%M %p")

    if current_time < appointment_datetime <= notification_72_hours:
        # Send a notification 72 hours before the appointment (FCM for Android)
        registration_id = 'your_fcm_registration_id'  # Replace with the FCM registration ID of the device
        message_title = "Appointment Reminder"
        message_body = f"Your appointment (ID: {appointment_id}) is scheduled in 72 hours."
        fcm_client.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    elif current_time < appointment_datetime <= notification_24_hours:
        # Send a notification 24 hours before the appointment (APNs for iOS)
        device_token = 'your_ios_device_token'  # Replace with the iOS device token
        message_body = f"Your appointment (ID: {appointment_id}) is scheduled in 24 hours."
        apns_client.send_notification(device_token, alert=message_body)

print("Notifications sent successfully.")

pip install pyfcm
pip install pyapns2

