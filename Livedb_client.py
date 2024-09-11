import random
import string
import sys
import requests

# server_address_="http://127.0.0.1:5000"
server_address_ = "https://livedb.pythonanywhere.com/"


class LiveDB:
    def __init__(self, user_code, server_address=server_address_):
        self.user_code = user_code
        self.server_address = server_address

    def insert(self, key, value):

        data = {"user_code": self.user_code, "key": key, "value": value}
        response = requests.post(f"{self.server_address}/insert_value", json=data)
        print(response.status_code)
        if response.status_code == 200:
            # if response[1] == 400:
            # print(response.json()[0]["message"])
            # sys.exit()
            return response.json()
        else:
            raise Exception(f"Error inserting data: {response.status_code}")

    def read(self, key):
        data = {"user_code": self.user_code, "key": key}
        response = requests.post(f"{self.server_address}/get_value", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error reading data: {response.status_code}")

    def delkey(self, key):
        data = {"user_code": self.user_code, "key": key}
        response = requests.post(f"{self.server_address}/delete_key", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error deleting key: {response.status_code}")

    def list(self):
        data = {"user_code": self.user_code}
        response = requests.post(f"{self.server_address}/listkeyvalues", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error reading list: {response.status_code}")


if __name__ == "__main__":
    user_code = "5e11a2dfbd484a67a5eaba98d5e1056d"
    # Create a new LiveDB client
    livedb = LiveDB(user_code)
    # print(livedb.list())
    # if livedb.list()["list"]:
    #     key_values = livedb.list()["key_value_pairs"]
    #     for i in key_values:
    #         print(i)
    # Create a new user

    print(livedb.insert("key1", "value1"))
    print(livedb.insert("key2", "testing_advanced"))

    # Read data
    value = livedb.read("key1")
    print(value)
    livedb.insert("key1", "test2")
    value = livedb.read("key1")
    print(value)
    # Delete a key
    livedb.delkey("key1")

    value = livedb.read("key1")
    print(value)
    print("------------------------")
    for i in range(1, 103):
        key = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(8)
        )
        value = f"Random value {i}"
        print(livedb.insert(key, value))
    value_pair = livedb.list()
    print(value_pair)
    print(livedb.insert("key2", "testing_advanced_3"))
    key_values = livedb.list()["key_value_pairs"]
    for i in key_values:
        print(i)
