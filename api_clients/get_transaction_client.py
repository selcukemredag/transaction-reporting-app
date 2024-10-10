from .base_api_client import BaseAPIClient

# Client for fetching details of a specific transaction
class GetTransactionClient(BaseAPIClient):
    # Initialize with the transaction ID
    def __init__(self, transaction_id):
        self.transaction_id = transaction_id

    # Return the API endpoint for getting a transaction
    def get_endpoint(self):
        return "https://sandbox-reporting.rpdpymnt.com/api/v3/transaction"

    # Return the request data to be sent to the API
    def get_request_data(self):
        return {
            "transactionId": self.transaction_id
        }
