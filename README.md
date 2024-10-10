# Transaction Reporting Application

A Flask web application that interacts with the Financial House Reporting API to fetch and display transaction reports, transaction details, and client information. The application includes an Ajax-based fluent interface for querying transactions.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Requirements](#project-requirements)

## Project Overview

This application serves as a client for the Financial House Reporting API. It allows users to:

- Generate transaction reports within a specified date range.
- Retrieve a list of transactions based on various filters.
- View detailed information about a specific transaction.
- Obtain client information associated with a transaction.
- Use an interactive web interface for querying transactions using an Ajax-based fluent approach.

## Project Requirements

Below is a list of the project requirements along with explanations of how each has been fulfilled.

1. **Transaction Report Generation**

   - **Requirement:** Create an endpoint that generates a transaction report based on a date range and optional merchant and acquirer IDs.
   - **Implementation:** Implemented the `/transactions/report` endpoint in `app.py` that accepts `fromDate`, `toDate`, `merchant`, and `acquirer` as query parameters. It uses the `TransactionReportClient` to fetch the report from the API.

2. **Transaction List with Filtering and Sorting**

   - **Requirement:** Provide an endpoint to list transactions with filtering options such as date range, status, operation, and more. Include sorting functionality.
   - **Implementation:** Created the `/transactions/list` endpoint in `app.py` that accepts various query parameters for filtering. Implemented filtering and sorting logic using list comprehensions and the `sorted()` function.

3. **Transaction Details Endpoint**

   - **Requirement:** Implement an endpoint to retrieve detailed information about a specific transaction using its ID.
   - **Implementation:** Added the `/transaction/<transaction_id>` endpoint in `app.py`. It uses the `GetTransactionClient` to fetch transaction details from the API.

4. **Client Information Endpoint**

   - **Requirement:** Provide an endpoint to obtain client information associated with a transaction.
   - **Implementation:** Implemented the `/client/<transaction_id>` endpoint in `app.py`. It uses the `GetClientInfoClient` to retrieve client information.

5. **Ajax-Based Fluent Interface (Optional)**

   - **Requirement:** Use an Ajax-based fluent approach for the transaction query endpoint to enhance user experience.
   - **Implementation:** Created a new HTML template `transactions.html` in the `templates` directory. It includes a form for inputting search parameters and uses jQuery to send Ajax requests to the `/transactions/list/ajax` endpoint. Results are displayed dynamically without page reloads.

6. **Best Practices for Error Handling and Code Organization**

   - **Requirement:** Follow best practices for error handling and organize code appropriately.
   - **Implementation:**
     - Used try-except blocks in `app.py` to handle exceptions and return meaningful error messages.
     - Organized API client classes in the `api_clients` package for modularity and reusability.
     - Used environment variables for sensitive information (credentials), managed with `python-dotenv`.

7. **Unit Testing**

   - **Requirement:** Write unit tests for the application.
   - **Implementation:** Created test cases in `tests/test_app.py` using `pytest`. Tests cover the main endpoints and check for correct responses and error handling.

8. **Version Control with GitHub**

   - **Requirement:** Use GitHub (or GitLab/Bitbucket) for version control.
   - **Implementation:** The project is managed using Git and hosted on GitHub for version control and collaboration.

9. **Deployment to Heroku**

   - **Requirement:** Deploy the application to Heroku for public access.
   - **Implementation:** Configured the application for deployment on Heroku, including a `Procfile`, managing environment variables.