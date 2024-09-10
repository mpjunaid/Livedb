import requests

# Replace with the actual server address (localhost for your local machine)
# server_address = "https://mpjunaid.pythonanywhere.com"
server_address = "http://127.0.0.1:5000"


# Send a GET request to the /db endpoint
response = requests.get(f"{server_address}/new_user")

# Check for successful response
if response.status_code == 200:
    # Convert JSON response to a Python dictionary
    data = response.json()
    print(f"Data from server: {data}")
else:
    print(f"Error accessing data: {response.status_code}")
