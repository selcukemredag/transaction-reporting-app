from flask import Flask, request, jsonify, render_template
# Import custom API clients
from api_clients.transaction_report_client import TransactionReportClient
from api_clients.transaction_list_client import TransactionListClient
from api_clients.get_transaction_client import GetTransactionClient
from api_clients.get_client_info_client import GetClientInfoClient
import json

# Initialize the Flask application
app = Flask(__name__)

# Define the home route
@app.route('/')
def home():
    # Render the index.html template
    return render_template('index.html')

# Define the route for fetching transaction reports
@app.route('/transactions/report', methods=['GET'])
def transactions_report():
    try:
        # Retrieve query parameters from the request URL
        from_date = request.args.get('fromDate', '2023-01-01')
        to_date = request.args.get('toDate', '2023-12-31')
        merchant = request.args.get('merchant')  # Optional parameter
        acquirer = request.args.get('acquirer')  # Optional parameter

        # Convert merchant and acquirer IDs to integers if provided
        merchant = int(merchant) if merchant else None
        acquirer = int(acquirer) if acquirer else None

        # Create an instance of the TransactionReportClient with the given parameters
        client = TransactionReportClient(from_date, to_date, merchant, acquirer)
        # Execute the API request
        response = client.execute()

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the JSON response data
            data = response.json()
            # Return the data as a JSON response
            return jsonify(data)
        else:
            # If the response is not successful, log and return an error message
            error_message = f"Failed to fetch transaction report. Status Code: {response.status_code}, Response: {response.text}"
            print(f"Error in transactions_report: {error_message}")
            return jsonify({"error": error_message}), response.status_code
    except Exception as e:
        # Handle any exceptions that occur during the process
        print(f"Exception in transactions_report: {e}")
        return jsonify({"error": str(e)}), 500

# Define the route for fetching a list of transactions
@app.route('/transactions/list', methods=['GET'])
def transactions_list():
    try:
        # Retrieve query parameters from the request URL
        params = {
            "fromDate": request.args.get('fromDate'),
            "toDate": request.args.get('toDate'),
            "status": request.args.get('status'),
            "operation": request.args.get('operation'),
            "merchantId": request.args.get('merchantId'),
            "acquirerId": request.args.get('acquirerId'),
            "paymentMethod": request.args.get('paymentMethod'),
            "errorCode": request.args.get('errorCode'),
            "filterField": request.args.get('filterField'),
            "filterValue": request.args.get('filterValue'),
            "page": request.args.get('page')
        }
        # Remove any parameters that are None or empty strings
        params = {k: v for k, v in params.items() if v}

        # Ensure that at least one parameter is provided
        if not params:
            return jsonify({"error": "At least one parameter must be provided."}), 400

        # Create an instance of the TransactionListClient with the given parameters
        client = TransactionListClient(params)
        # Execute the API request
        response = client.execute()

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the JSON response data
            transaction_data = response.json()
            data = transaction_data.get('data', [])

            # Data Structures and Algorithms Implementation
            # Filter transactions where the original amount is greater than 100 and status is 'APPROVED'
            filtered_transactions = [
                txn for txn in data
                if txn.get('transaction', {}).get('merchant', {}).get('originalAmount', 0) > 100 and
                   txn.get('transaction', {}).get('status') == 'APPROVED'
            ]
            # Sort the filtered transactions by original amount in descending order
            sorted_transactions = sorted(
                filtered_transactions,
                key=lambda x: x.get('transaction', {}).get('merchant', {}).get('originalAmount', 0),
                reverse=True
            )
            # Return the sorted transactions as a JSON response
            return jsonify(sorted_transactions)
        else:
            # If the response is not successful, log and return an error message
            error_message = f"Failed to fetch transaction list. Status Code: {response.status_code}, Response: {response.text}"
            print(f"Error in transactions_list: {error_message}")
            return jsonify({"error": error_message}), response.status_code
    except Exception as e:
        # Handle any exceptions that occur during the process
        print(f"Exception in transactions_list: {e}")
        return jsonify({"error": str(e)}), 500

# Define the route for fetching details of a specific transaction
@app.route('/transaction/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    try:
        # Create an instance of the GetTransactionClient with the given transaction ID
        client = GetTransactionClient(transaction_id)
        # Execute the API request
        response = client.execute()

        # Parse the JSON response data
        data = response.json()

        # Check if the response is successful and the status is 'APPROVED'
        if response.status_code == 200 and data.get('status') == 'APPROVED':
            # Return the transaction data as a JSON response
            return jsonify(data)
        else:
            # If not successful, log and return the error message from the API
            error_message = data.get('message', 'Unknown error')
            print(f"Error in get_transaction: {error_message}")
            return jsonify({"error": error_message}), 400
    except Exception as e:
        # Handle any exceptions that occur during the process
        print(f"Exception in get_transaction: {e}")
        return jsonify({"error": str(e)}), 500

# Define the route for fetching client information associated with a transaction
@app.route('/client/<transaction_id>', methods=['GET'])
def get_client(transaction_id):
    try:
        # Create an instance of the GetClientInfoClient with the given transaction ID
        client = GetClientInfoClient(transaction_id)
        # Execute the API request
        response = client.execute()

        # Print the raw response text for debugging purposes
        print(f"Raw response text: {response.text}")

        # Attempt to parse the response as JSON
        try:
            # Try parsing the response text directly
            data = json.loads(response.text)
        except json.JSONDecodeError:
            # If parsing fails, handle double-encoded JSON
            response_text = response.text.strip('"').replace('\\"', '"')
            data = json.loads(response_text)

        # Check if the response is successful and contains 'customerInfo'
        if response.status_code == 200 and data.get('customerInfo'):
            # Return the client information as a JSON response
            return jsonify(data)
        else:
            # If not successful, log and return the error message from the API
            error_message = data.get('message', 'Unknown error')
            print(f"Error in get_client: {error_message}")
            return jsonify({"error": error_message}), 400
    except Exception as e:
        # Handle any exceptions that occur during the process
        print(f"Exception in get_client: {e}")
        return jsonify({"error": str(e)}), 500

# Run the Flask application when this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)