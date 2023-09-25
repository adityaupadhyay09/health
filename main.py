import json
from azure.servicebus import ServiceBusService
from azure.servicebus import Message
from azure.mgmt.notificationhubs import NotificationHubsManagementClient
from plyer import notification
import datetime

# Azure Notification Hub configuration
namespace = 'YourNamespace'
hub_name = 'YourHubName'
shared_access_key_name = 'YourAccessKeyName'
shared_access_key_value = 'YourAccessKeyValue'

# Create a ServiceBusService client
bus_service = ServiceBusService(
    service_namespace=namespace,
    shared_access_key_name=shared_access_key_name,
    shared_access_key_value=shared_access_key_value
)

# Notification message to be sent
notification_message = Message("Your Notification Message")

# Specify a tag to target a specific device or user
notification_message.custom_properties['tag'] = 'YourTag'

# Send the notification using Service Bus
bus_service.send_notification(hub_name, notification_message)

# Azure Notification Hub configuration
connection_string = "your_connection_string"
hub_name = "your_hub_name"

# Dictionary to store booked appointments for different users (in a real application, this data would be stored in a database)
booked_appointments = {
    'user1': [
        datetime.datetime(2023, 9, 30, 10, 0),
        datetime.datetime(2023, 10, 5, 15, 30),
    ],
    'user2': [
        datetime.datetime(2023, 9, 30, 13, 0),
        datetime.datetime(2023, 10, 1, 9, 0),
    ],
}

# Simulate user login (replace this with your actual user authentication logic)
logged_in_user = 'user1'  # This represents the user who has logged in

# Get the current date and time
current_time = datetime.datetime.now()

# Check if the user has any appointments for the current date
if logged_in_user in booked_appointments:
    for appointment_date in booked_appointments[logged_in_user]:
        if current_time.date() == appointment_date.date():
            # Calculate the time until the appointment
            time_until_appointment = appointment_date - current_time

            # Convert the time until the appointment to seconds
            time_until_appointment_seconds = time_until_appointment.total_seconds()

            if time_until_appointment_seconds > 0:
                # Calculate the number of seconds until the appointment
                seconds_until_appointment = int(time_until_appointment_seconds)

                # Convert seconds to minutes and hours
                minutes_until_appointment, seconds_until_appointment = divmod(seconds_until_appointment, 60)
                hours_until_appointment, minutes_until_appointment = divmod(minutes_until_appointment, 60)

                # Create a notification message
                notification_title = "Appointment Reminder"
                notification_message = f"Your appointment is in {hours_until_appointment} hours and {minutes_until_appointment} minutes."

                # Send the notification using Plyer (local notification)
                notification.notify(
                    title=notification_title,
                    message=notification_message,
                    timeout=10  # Display the notification for 10 seconds
                )

                # Send the notification to Azure Notification Hub
                hub_service = NotificationHubsManagementClient(connection_string, hub_name)
                hub_service.send_notification(
                    tags=[logged_in_user],
                    message=notification_message,
                )
else:
    print("No appointments found for the logged-in user.")


