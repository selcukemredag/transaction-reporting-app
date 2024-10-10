from .base_api_client import BaseAPIClient

# Client for fetching transaction reports
class TransactionReportClient(BaseAPIClient):
    # Initialize with from_date, to_date, and optional merchant and acquirer IDs
    def __init__(self, from_date, to_date, merchant=None, acquirer=None):
        self.from_date = from_date
        self.to_date = to_date
        self.merchant = merchant
        self.acquirer = acquirer

    # Return the API endpoint for transaction reports
    def get_endpoint(self):
        return "https://sandbox-reporting.rpdpymnt.com/api/v3/transactions/report"

    # Return the request data to be sent to the API
    def get_request_data(self):
        data = {
            "fromDate": self.from_date,
            "toDate": self.to_date
        }
        # Include merchant and acquirer IDs if provided
        if self.merchant is not None:
            data["merchant"] = self.merchant
        if self.acquirer is not None:
            data["acquirer"] = self.acquirer
        return data
