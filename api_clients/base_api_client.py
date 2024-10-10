from abc import ABC, abstractmethod
import requests
from auth import get_jwt_token

# Base class for all API clients, using the Abstract Base Class (ABC) module
class BaseAPIClient(ABC):
    # Abstract method to get the endpoint URL
    @abstractmethod
    def get_endpoint(self):
        pass

    # Abstract method to get the request data
    @abstractmethod
    def get_request_data(self):
        pass

    # Method to execute the API request
    def execute(self):
        try:
            # Retrieve the JWT token for authentication
            token = get_jwt_token()
            # Set up the headers with the Authorization token
            headers = {"Authorization": token}
            # Get the endpoint URL
            url = self.get_endpoint()
            # Get the request data
            data = self.get_request_data()

            # Debug: Print the data being sent for transparency
            print(f"Sending request to {url} with data: {data} and headers: {headers}")

            # Make the POST request to the API
            response = requests.post(url, headers=headers, json=data)
            # Return the response object
            return response
        except Exception as e:
            # Handle any exceptions that occur during the request
            print(f"Exception in API client execute method: {e}")
            raise
