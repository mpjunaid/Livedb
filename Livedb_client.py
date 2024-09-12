import random
import string
import sys
import requests

server_address_ = "http://127.0.0.1:5000"
# server_address_ = "https://livedb.pythonanywhere.com/"


class LiveDB:
    def __init__(self, user_code, server_address=server_address_):
        self.server_address = server_address
        self.user_code = user_code

        url = f"{self.server_address}/db_status"
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print("Database is not active.")
            sys.exit(1)

        data = {"user_code": self.user_code}
        response = requests.post(f"{self.server_address}/user_status", json=data)
        if response.status_code == 200:
            json_data = response.json()
            if json_data["user_status"]:
                print("User not found")
                sys.exit(1)
        else:
            raise Exception(f"Error checking for data: {response.status_code}")

    def insert(self, key, value):

        data = {"user_code": self.user_code, "key": key, "value": value}
        response = requests.post(f"{self.server_address}/insert_value", json=data)
        if response.status_code == 200:
            json_data = response.json()
            if not json_data["result"]:
                print(json_data["message"])
                sys.exit(1)
            else:
                return True
        else:
            raise Exception(f"Error inserting data: {response.status_code}")

    def read(self, key):
        data = {"user_code": self.user_code, "key": key}
        response = requests.post(f"{self.server_address}/get_value", json=data)
        if response.status_code == 200:
            json_data = response.json()
            if not json_data["result"]:
                print(json_data["message"])
                sys.exit(1)
            else:
                return True
        else:
            raise Exception(f"Error reading data: {response.status_code}")

    def delkey(self, key):
        data = {"user_code": self.user_code, "key": key}
        response = requests.post(f"{self.server_address}/delete_key", json=data)
        if response.status_code == 200:
            json_data = response.json()
            if not json_data["result"]:
                print(json_data["message"])
                sys.exit(1)
            else:
                return True
        else:
            raise Exception(f"Error deleting key: {response.status_code}")

    def delete_user_keys(self):
        data = {"user_code": self.user_code}
        response = requests.post(f"{self.server_address}/delete_user_keys", json=data)
        if response.status_code == 200:
            json_data = response.json()
            if not json_data["result"]:
                print(json_data["message"])
                sys.exit(1)
            else:
                return True
        else:
            raise Exception(f"Error deleting key: {response.status_code}")

    def list(self):
        data = {"user_code": self.user_code}
        response = requests.post(f"{self.server_address}/listkeyvalues", json=data)
        if response.status_code == 200:
            json_data = response.json()
            if not json_data["result"]:
                print(json_data["message"])
                sys.exit(1)
            else:
                return json_data["key_value_pairs"]
        else:
            raise Exception(f"Error reading list: {response.status_code}")


if __name__ == "__main__":
    user_code = "62c4163caa044745a3cf2f26b42228c8"
    livedb = LiveDB(user_code)
    values = livedb.list()
    for i in values:
        print(i)
    livedb.insert("vake0c52", "Testing")
    print(livedb.read("vake0c52"))
    values = livedb.list()
    for i in values:
        print(i)
