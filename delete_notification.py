import os
import datetime
from pyfcm import FCMNotification

# Firebase Cloud Messaging (FCM) configuration
fcm_api_key = 'your_fcm_api_key'  # Replace with your FCM API key

# Initialize FCM client
fcm_client = FCMNotification(api_key=fcm_api_key)

# Calculate notification schedule times
current_time = datetime.datetime.utcnow()

# Query your data source to get appointment information (replace this with your data retrieval logic)
def get_appointments():
    appointments = [
        {
            'appointment_id': 1,
            'patient_id': 'patient_1',
            'appointment_date': '10/15/2023',
            'appointment_time': '10:00 AM',
            # Add more fields as needed
        },
        # Add more appointments
    ]
    return appointments

# Get appointments from your data source
appointments = get_appointments()

# Send notifications
for appointment in appointments:
    appointment_id = appointment['appointment_id']
    appointment_date = appointment['appointment_date']
    appointment_time = appointment['appointment_time']

    appointment_datetime = datetime.datetime.strptime(f"{appointment_date} {appointment_time}", "%m/%d/%Y %I:%M %p")

    if current_time < appointment_datetime:
        # Calculate the time difference between the appointment and the current time
        time_difference = appointment_datetime - current_time

        # Send a notification 72 hours before the appointment
        if time_difference <= datetime.timedelta(hours=72):
            registration_id = 'your_fcm_registration_id'  # Replace with the FCM registration ID of the device
            message_title = "Appointment Reminder"
            message_body = f"Your appointment (ID: {appointment_id}) is scheduled in 72 hours."

            # Send the notification
            result = fcm_client.notify_single_device(
                registration_id=registration_id,
                message_title=message_title,
                message_body=message_body,
            )

            # Check if the notification was sent successfully
            if result['success'] == 1:
                print(f"Notification sent for appointment (ID: {appointment_id})")

print("Notifications sent successfully.")

