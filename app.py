from flask import Flask, jsonify, request, render_template
from utility_functions import generate_unique_string
from database import Livedb


port = 5000  # Global parameter

db = {}

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("home.html")


@app.route("/sign_up", methods=["POST"])
def sign_up():
    database = Livedb()
    email = request.form.get("email")
    user_code, success = database.insert_user(email)

    data = {"key": user_code, "created": success}
    database.close_connection()

    return jsonify(data)


@app.route("/db_status")
def db_status():
    data = {"status": "Active"}
    return jsonify(data)


# @app.route("/new_user")
# def new_user():
#     temp_user_code = generate_unique_string(db.keys())
#     data = {"code": temp_user_code, "user_created": True}
#     db[temp_user_code] = {"code": temp_user_code, "data": {}}
#     return jsonify(data)


@app.route("/insert_value", methods=["POST"])
def insert_value():
    database = Livedb()

    user = request.json.get("user_code")
    key = request.json.get("key")
    value = request.json.get("value")

    if not user or not key or not value:
        return jsonify(
            {"message": "Missing required data (user_code, key, or value)"}, 400
        )
    exists, num_keys = database.user_exist(user)

    if exists:
        return jsonify({"message": "Invalid user code"}, 400)
    if user not in db:
        db[user] = {"code": user, "data": {}}
    if len(db[user]["data"]) > num_keys and key not in db[user]["data"]:
        return jsonify(
            {"message": "Maximum number of keys are reached. Please delete some"}, 400
        )

    db[user]["data"][key] = value
    database.update_last_used(user)
    database.close_connection()
    return jsonify({"message": True})


@app.route("/get_value", methods=["POST"])
def get_value():
    user_code = request.json.get("user_code")
    key = request.json.get("key")

    if not user_code or not key:
        return jsonify({"message": "Missing required data (user_code or key)"}, 400)

    if user_code not in db:
        return jsonify({"message": "Invalid user code"}, 400)

    user_data = db[user_code]["data"]
    value = user_data.get(key)

    if value is None:
        return jsonify({"message": "Key not found for the user"}, 404)

    return jsonify({"Message": value})


@app.route("/delete_key", methods=["POST"])
def delete_key():
    user_code = request.json.get("user_code")
    key = request.json.get("key")

    if not user_code or not key:
        return jsonify({"message": "Missing required data (user_code or key)"}, 400)

    if user_code not in db:
        return jsonify({"message": "Invalid user code"}, 400)

    user_data = db[user_code]["data"]

    if key not in user_data:
        return jsonify({"message": "Key not found for the user"}, 404)

    del user_data[key]  # Delete the key from the user's data

    return jsonify({"message": "Key deleted successfully"}, 200)


@app.route("/delete_user", methods=["POST"])
def delete_user():
    user_code = request.json.get("user_code")

    if not user_code:
        return jsonify({"message": "Missing required data (user_code)"}, 400)

    if user_code not in db:
        return jsonify({"message": "Invalid user code"}, 400)

    del db[user_code]  # Delete the user from the database

    return jsonify({"message": "User deleted successfully"})


@app.route("/listkeyvalues", methods=["POST"])
def list_key_values():
    user_code = request.json.get("user_code")

    if not user_code:
        return jsonify({"message": "Missing required data (user_code)"}, 400)

    if user_code not in db:
        return jsonify({"message": "Invalid user code"}, 400)

    user_data = db.get(user_code, {}).get(
        "data", {}
    )  # Handle missing user and data gracefully
    key_value_pairs = list(user_data.items())  # Convert dictionary to a list of tuples
    if len(key_value_pairs > 0):
        status = True
    else:
        status = False
    return jsonify({"key_value_pairs": key_value_pairs, "list": status})


if __name__ == "__main__":
    app.run(port=port)
