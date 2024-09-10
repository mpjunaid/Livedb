import requests


class LiveDB:
    """Client class for interacting with the Livedb server."""

    def __init__(self, server_address="http://127.0.0.1:5000"):
        """
        Initializes the LiveDB client with the server address.

        Args:
            server_address (str, optional): The address of the Livedb server. Defaults to "http://127.0.0.1:5000".
        """
        self.server_address = server_address

    def new_user(self):
        """
        Sends a request to the server to create a new user.

        Returns:
            dict: A dictionary containing the user code and a flag indicating successful creation.
                  Example: {"code": "USER_CODE", "user_created": True}
        """
        response = requests.get(f"{self.server_address}/new_user")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error creating new user: {response.status_code}")

    def insert(self, user_code, key, value):
        """
        Inserts a key-value pair into a user's data on the server.

        Args:
            user_code (str): The user code retrieved from `new_user`.
            key (str): The key for the data.
            value (str): The value to be associated with the key.

        Returns:
            dict: A dictionary containing a success message if the insertion was successful.
                  Example: {"message": True}
        """
        data = {"user_code": user_code, "key": key, "value": value}
        response = requests.post(f"{self.server_address}/insert_value", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error inserting data: {response.status_code}")

    def read(self, user_code, key):
        """
        Reads the value associated with a key for a user from the server.

        Args:
            user_code (str): The user code.
            key (str): The key for the data.

        Returns:
            dict: A dictionary containing the value associated with the key, or an error message if not found.
                  Example: {"value": "YOUR_VALUE"} or {"message": "Key not found for the user"}
        """
        data = {"user_code": user_code, "key": key}
        response = requests.post(f"{self.server_address}/get_value", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error reading data: {response.status_code}")

    def delkey(self, user_code, key):
        """
        Deletes a key-value pair from a user's data on the server.

        Args:
            user_code (str): The user code.
            key (str): The key to be deleted.

        Returns:
            dict: A dictionary containing a success message if the deletion was successful.
                  Example: {"message": "Key deleted successfully"}
        """
        data = {"user_code": user_code, "key": key}
        response = requests.post(f"{self.server_address}/delete_key", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error deleting key: {response.status_code}")

    def deluser(self, user_code):
        """
        Deletes a user from the server.

        Args:
            user_code (str): The user code to be deleted.

        Returns:
            dict: A dictionary containing a success message if the user was deleted successfully.
                  Example: {"message": "User deleted successfully"}
        """
        data = {"user_code": user_code}
        response = requests.post(f"{self.server_address}/delete_user", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error deleting user: {response.status_code}")


if __name__ == "__main__":
    # Create a new LiveDB client
    livedb = LiveDB()

    # Create a new user
    new_user_response = livedb.new_user()
    print("New user response:", new_user_response)

    # Insert data
    user_code = new_user_response["code"]
    livedb.insert(user_code, "key1", "value1")
    livedb.insert(user_code, "key2", "value2")

    # Read data
    value = livedb.read(user_code, "key1")
    print("Read value:", value)

    # Delete a key
    livedb.delkey(user_code, "key1")

    # Check if the key is deleted
    value = livedb.read(user_code, "key2")
    print("Read value after deletion:", value)

    # Delete the user
    livedb.deluser(user_code)

    # Try to read data from the deleted user
    try:
        value = livedb.read(user_code, "key1")
        print("Read value from deleted user:", value)
    except Exception as e:
        print("Error reading value from deleted user:", e)
