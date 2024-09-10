import requests

server_address = "http://127.0.0.1:5000"

# Prepare the data to send (replace with your actual values)
user_code = "FNrSEmGmVY"  # Replace with the user code you received from the server
key = "your_key"  # Replace with the key you want to insert
value = "your_value"  # Replace with the value you want to insert

# Send a POST request to the /insert_value endpoint with data in the request body
data = {"user_code": user_code, "key": key, "value": value}
response = requests.post(f"{server_address}/insert_value", json=data)

# Check for successful response
if response.status_code == 200:
    # Get response data (if any)
    response_data = response.json()
    print(f"Response from server: {response_data}")
else:
    print(f"Error sending data: {response.status_code}")
