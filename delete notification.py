import os
import datetime
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
from pyfcm import FCMNotification
from pyapns2.client import APNsClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import asyncio

# Azure credentials and configuration
subscription_id = 'your_subscription_id'
resource_group_name = 'your_resource_group'
cosmosdb_account_name = 'your_cosmosdb_account_name'
cosmosdb_database_name = 'your_cosmosdb_database_name'
cosmosdb_container_name = 'your_cosmosdb_container_name'

# Firebase Cloud Messaging (FCM) configuration
fcm_api_key = 'your_fcm_api_key'  # Replace with your FCM API key

# Apple Push Notification Service (APNs) configuration
apns_cert_file = 'your_apns_cert.pem'  # Replace with the path to your APNs certificate file
apns_key_file = 'your_apns_key.pem'    # Replace with the path to your APNs key file

# Initialize Azure Cosmos DB client
credential = DefaultAzureCredential()
cosmos_client = CosmosClient(account_url=f'https://{cosmosdb_account_name}.documents.azure.com:443/',
                             credential=credential)

# Calculate notification schedule times
current_time = datetime.datetime.utcnow()

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

# Send notifications and schedule deletion
for appointment in appointments:
    appointment_id = appointment['appointment_id']
    patient_id = appointment['patient_id']
    appointment_date = appointment['appointment_date']
    appointment_time = appointment['appointment_time']

    appointment_datetime = datetime.datetime.strptime(f"{appointment_date} {appointment_time}", "%m/%d/%Y %I:%M %p")

    if current_time < appointment_datetime <= notification_72_hours:
        # Calculate expiration time (e.g., 72 hours after the appointment)
        expiration_time = appointment_datetime + datetime.timedelta(hours=72)

        # Send a notification 72 hours before the appointment (FCM for Android)
        registration_id = 'your_fcm_registration_id'  # Replace with the FCM registration ID of the device
        message_title = "Appointment Reminder"
        message_body = f"Your appointment (ID: {appointment_id}) is scheduled in 72 hours."

        # Send the notification with expiration time
        fcm_client.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, time_to_live=expiration_time)

        # Schedule the deletion of the 72-hour notification
        notification_tag_72_hours = f'appointment_72_hours_{appointment_id}'  # Unique identifier for the 72-hour notification
        async def delete_notification(notification_tag):
            with ServiceBusClient.from_connection_string("your_connection_string") as client:
                with client.get_queue_sender("your_queue_name") as sender:
                    message = ServiceBusMessage(body=f"Delete notification with tag: {notification_tag}")
                    await sender.send_messages(message)

        # Asynchronously delete the 72-hour notification
        asyncio.run(delete_notification(notification_tag_72_hours))
        print(f"Deleting 72-hour notification for appointment (ID: {appointment_id})")

    elif current_time < appointment_datetime <= notification_24_hours:
        # Calculate expiration time (e.g., 24 hours after the appointment)
        expiration_time = appointment_datetime + datetime.timedelta(hours=24)

        # Send a notification 24 hours before the appointment (APNs for iOS)
        device_token = 'your_ios_device_token'  # Replace with the iOS device token
        message_body = f"Your appointment (ID: {appointment_id}) is scheduled in 24 hours."

        # Send the notification with expiration time
        apns_client.send_notification(device_token, alert=message_body, expiration=expiration_time)

        # Schedule the deletion of the 24-hour notification
        notification_tag_24_hours = f'appointment_24_hours_{appointment_id}'  # Unique identifier for the 24-hour notification
        async def delete_notification(notification_tag):
            with ServiceBusClient.from_connection_string("your_connection_string") as client:
                with client.get_queue_sender("your_queue_name") as sender:
                    message = ServiceBusMessage(body=f"Delete notification with tag: {notification_tag}")
                    await sender.send_messages(message)

        # Asynchronously delete the 24-hour notification
        asyncio.run(delete_notification(notification_tag_24_hours))
        print(f"Deleting 24-hour notification for appointment (ID: {appointment_id})")

    elif current_time >= appointment_datetime:
        # Calculate expiration time (e.g., immediately)
        expiration_time = current_time

        # Delete the notification after the appointment time has passed
        notification_tag = f'appointment_{appointment_id}'  # Replace with an appropriate tag or identifier
        async def delete_notification(notification_tag):
            with ServiceBusClient.from_connection_string("your_connection_string") as client:
                with client.get_queue_sender("your_queue_name") as sender:
                    message = ServiceBusMessage(body=f"Delete notification with tag: {notification_tag}")
                    await sender.send_messages(message)

        # Asynchronously delete the notification
        asyncio.run(delete_notification(notification_tag))
        print(f"Deleting notification for appointment (ID: {appointment_id})")

print("Notifications sent and deletion scheduled successfully.")


