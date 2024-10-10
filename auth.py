from threading import Lock
import time
import requests
import os

# Global variables for token management
TOKEN = None
TOKEN_EXPIRY = 0
TOKEN_LOCK = Lock()

# Function to get the JWT token for authentication
def get_jwt_token():
    global TOKEN, TOKEN_EXPIRY

    with TOKEN_LOCK:
        # Get the current time
        current_time = time.time()
        # Check if the token is valid and not expired
        if TOKEN and TOKEN_EXPIRY > current_time:
            # Return the existing token
            return TOKEN

        # Endpoint for merchant login
        url = "https://sandbox-reporting.rpdpymnt.com/api/v3/merchant/user/login"
        # Credentials for authentication
        credentials = {
            "email": os.environ.get("MERCHANT_EMAIL"),
            "password": os.environ.get("MERCHANT_PASSWORD")
        }

        try:
            # Make the POST request to get the token
            response = requests.post(url, json=credentials)
            if response.status_code == 200:
                # Parse the response to get the token
                data = response.json()
                TOKEN = data.get("token")
                # Set the token expiry time (10 minutes from now)
                TOKEN_EXPIRY = current_time + 600  # Token is valid for 10 minutes
                # Return the new token
                return TOKEN
            else:
                # Log the error if authentication fails
                print(f"Authentication failed. Status Code: {response.status_code}, Response: {response.text}")
                raise Exception(f"Authentication failed. Status Code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            # Handle exceptions that occur during the request
            print(f"Exception during authentication request: {e}")
            raise Exception(f"Exception during authentication request: {e}")
