# Livedb: Your Effortless Key-Value Storage Solution

Livedb simplifies storing and retrieving key-value pairs with minimal setup.

Access your data from anywhere using HTTP requests and integrate it into your projects with pre-built libraries.

### Key Features

- **Global Accessibility:** Access data from any internet-connected device.

- **Simplified Integration:** Use pre-built libraries for JavaScript, Python, and Go (JavaScript and Go libraries are under development).

- **Rapid Development:** Store and retrieve data with minimal code.

## LiveDB Class: Instruction Manual

LiveDB is a Python class for interacting with a remote database service. It provides functionalities for CRUD (Create, Read, Update, Delete) operations on key-value pairs associated with a unique user code.

### Prerequisites

- Python 3.x
- requests library (installation: pip install requests)

### Obtaining User Code

- Visit https://livedb.pythonanywhere.com/.
  -Register with your email address.
  -You'll receive an email containing your unique user code.

      Important Note: User data are automatically deleted if inactive for three consecutive days.

### Installation

1. Dowload the `Livedb_client.py` file the guthub repo.(You can copy paste too)
2. `from Livedb_cleint import livedb`

### Using LiveDB for CRUD operations

1. Initialization

Replace <your_user_code> with your user code from the registration email:

```Python
from Livedb_cleint import liveDB
user_code = "<your_user_code>"
livedb = LiveDB(user_code)

```

Returns a class object of LiveDB class on success. Otherwise an error message if the user_code is not valid or if the livedb server is down.

2. Create (Insert):

Stores a new key-value pair.

```Python
key = "new_key"
value = "This is some new data"
livedb.insert(key, value)
```

Returns True on success. Otherwise, an error message is printed.

3. Read (Get):

Retrieves the value associated with a specific key.

```
Python
key = "existing_key"
retrieved_value = livedb.read(key)
```

Returns the value if the key exists. Otherwise, an error message is printed.

4. Update (Not directly supported):

LiveDB doesn't have a direct update method. To modify existing data just use the same create/insert function. If the key already exist it gets updated.

5. Delete (Delete Key):

Removes a key-value pair from the database.

```Python
key = "key_to_delete"
livedb.delkey(key)
```

Returns True on success. Otherwise, an error message is printed.

6. Listing All Key-Value Pairs

Retrieves a list of all key-value pairs associated with your user code.

```Python
all_values = livedb.list()
for key_value_pair in all_values:
    print(key_value_pair)
```

7. Deleting All User Keys

Permanently removes all key-value pairs associated with your user code.

```Python
livedb.delete_user_keys()
```

Returns True on success. Otherwise, an error message is printed.
