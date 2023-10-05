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

            # Create a data payload for the toast notification
            data_payload = {
                'title': message_title,
                'body': message_body,
                'click_action': 'OPEN_ACTIVITY',  # Add an action to open a specific activity when the notification is clicked
                'appointment_id': str(appointment_id),  # You can include additional data
            }

            # Send the notification with the data payload
            result = fcm_client.single_device_data_message(registration_id=registration_id, data_message=data_payload)

            # Check if the notification was sent successfully
            if result['success'] == 1:
                print(f"Notification sent for appointment (ID: {appointment_id})")

print("Notifications sent successfully.")






# kotlin action
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class YourActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.your_activity_layout)

        // Handle the click action from the notification
        if (intent?.action == "OPEN_ACTIVITY") {
            // Perform actions to open the desired activity
            // For example, you can start a new activity:
            // startActivity(Intent(this, YourDesiredActivity::class.java))
        }
    }
}

