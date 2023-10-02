import azure.functions as func
import requests
import hashlib
import time
import json

# Define global variables for storing the access token and its expiration time
access_token = None
expiration_time = 0

# Define the duration of an access token's validity in seconds (86399 seconds = approximately 24 hours)
ACCESS_TOKEN_DURATION = 86399

def generate_access_token():
    global access_token
    global expiration_time

    api_url = "https://apisandbox.mdflow.com/MDFEHRAPI/api/security/login"
    grant_type = "password"
    x_auth_username = "ERH_Centrum"
    x_auth_timestamp = str(int(time.time()))
    x_auth_nonce = "648db976-6428-459d-873e-891169e5a4e2"

    concatenated_string = f"JOtcVaObKu3l:{x_auth_nonce}:{x_auth_timestamp}"
    x_auth_password_digest = hashlib.sha256(concatenated_string.encode()).hexdigest()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": grant_type,
        "X-Auth-Username": x_auth_username,
        "X-Auth-Timestamp": x_auth_timestamp,
        "X-Auth-Nonce": x_auth_nonce,
        "X-Auth-PasswordDigest": x_auth_password_digest,
    }

    response = requests.post(api_url, headers=headers, data=data)

    if response.status_code == 200:
        # Parse the response to get the access token
        response_data = json.loads(response.content.decode())
        access_token = response_data.get("access_token")
        expiration_time = time.time() + ACCESS_TOKEN_DURATION
        print(f"Access Token: {access_token}")
        print(f"Expiration Time: {expiration_time} seconds")

def main(req: func.HttpRequest) -> func.HttpResponse:
    global access_token
    global expiration_time

    current_time = time.time()

    # Check if the access token is not set or has expired
    if access_token is None or current_time >= expiration_time:
        print("Generating a new access token...")
        generate_access_token()

    return func.HttpResponse(
        f"Access Token: {access_token}",
        mimetype="text/plain",
    )
