import azure.functions as func
import requests
import hashlib
import time

# Variables for the access token
api_url = "https://apisandbox.mdflow.com/MDFEHRAPI/api/security/login"
grant_type = "password"
x_auth_username = "ERH_Centrum"
x_auth_nonce = "648db976-6428-459d-873e-891169e5a4e2"
access_token = None
token_expiration_time = None

def get_access_token():
    global access_token, token_expiration_time
    
    # Check if we have a cached access token and it's still valid
    if access_token and token_expiration_time and token_expiration_time > time.time():
        return access_token
    
    x_auth_timestamp = str(int(time.time()))
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
        response_data = response.json()
        access_token = response_data.get("access_token")
        expires_in = response_data.get("expires_in", 86400)  # Default to 86400 seconds if expires_in is not provided
        token_expiration_time = time.time() + expires_in
        return access_token
    
    return None

def main(req: func.HttpRequest) -> func.HttpResponse:
    access_token = get_access_token()
    
    if access_token:
        return func.HttpResponse(f"Access Token: {access_token}", mimetype="text/plain")
    else:
        return func.HttpResponse("Failed to retrieve access token", status_code=500)

