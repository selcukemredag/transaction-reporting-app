import pytest
from app import app

# Define a fixture for the Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test the transactions report endpoint
def test_transactions_report(client):
    # Send a GET request to the '/transactions/report' endpoint
    response = client.get('/transactions/report')
    # Print the response data for debugging
    print(response.data)
    # If there is an error, print the server error message
    if response.status_code in [400, 500]:
        print(f"Server Error: {response.data.decode('utf-8')}")
    # Assert that the response status code is 200 (OK) or 401 (Unauthorized)
    assert response.status_code in [200, 401]

# Test the transactions list endpoint
def test_transactions_list(client):
    # Send a GET request with query parameters to the '/transactions/list' endpoint
    response = client.get('/transactions/list?fromDate=2015-07-01&toDate=2015-10-01')
    # Print the response data for debugging
    print(response.data)
    # If there is an error, print the server error message
    if response.status_code in [400, 500]:
        print(f"Server Error: {response.data.decode('utf-8')}")
    # Assert that the response status code is 200 (OK) or 401 (Unauthorized)
    assert response.status_code in [200, 401]

# Test the get transaction endpoint
def test_get_transaction(client):
    # Use a valid transaction ID for testing
    transaction_id = '1-1444392550-1'  # Replace with a valid transaction ID if necessary
    # Send a GET request to the '/transaction/<transaction_id>' endpoint
    response = client.get(f'/transaction/{transaction_id}')
    # Parse the JSON response data
    data = response.get_json()
    # Print the data for debugging
    print(data)
    # Assert that the response status code is acceptable
    assert response.status_code in [200, 400, 401, 404]
    if response.status_code == 200:
        # If successful, ensure 'transaction' is in the response data
        assert 'transaction' in data
    else:
        # If not successful, ensure 'error' is in the response data
        assert 'error' in data

# Test the get client endpoint
def test_get_client(client):
    # Use a valid transaction ID for testing
    transaction_id = '1-1444392550-1'  # Replace with a valid transaction ID if necessary
    # Send a GET request to the '/client/<transaction_id>' endpoint
    response = client.get(f'/client/{transaction_id}')
    # Parse the JSON response data
    data = response.get_json()
    # Print the data for debugging
    print(data)
    # Assert that the response status code is acceptable
    assert response.status_code in [200, 400, 401, 404, 500]
    if response.status_code == 200:
        # If successful, ensure 'customerInfo' is in the response data
        assert 'customerInfo' in data  # Adjust based on expected data structure
    else:
        # If not successful, ensure 'error' is in the response data
        assert 'error' in data
