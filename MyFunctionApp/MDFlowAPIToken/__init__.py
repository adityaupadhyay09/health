
import azure.functions as func
import requests
import hashlib
import time

def main(req: func.HttpRequest) -> func.HttpResponse:
    api_url = "https://apisandbox.mdflow.com/MDFEHRAPI/api/security/login"
    grant_type = "password"
    x_auth_username = "ERH_Centrum"
    x_auth_timestamp = str(int(time.time()))
    x_auth_nonce = "648db976-6428-459d-873e-891169e5a4e2"

    concatenated_string = f"JOtcVaObKu3l:{x_auth_nonce}:{x_auth_timestamp}"
    x_auth_password_digest = hashlib.sha256(concatenated_string.encode()).hexdigest()
    
    print(f"x-auth-timestamp: {x_auth_timestamp}")
    print(f"X-Auth-PasswordDigest: {x_auth_password_digest}")

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

    return func.HttpResponse(
        f"Response Status Code: {response.status_code}\nResponse Content: {response.content.decode()}",
        mimetype="text/plain",
    )
