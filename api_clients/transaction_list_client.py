from .base_api_client import BaseAPIClient

# Client for fetching a list of transactions
class TransactionListClient(BaseAPIClient):
    # Initialize with the query parameters
    def __init__(self, params):
        self.params = params

    # Return the API endpoint for transaction list
    def get_endpoint(self):
        return "https://sandbox-reporting.rpdpymnt.com/api/v3/transaction/list"

    # Return the request data to be sent to the API
    def get_request_data(self):
        return self.params
