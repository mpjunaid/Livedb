from flask import Flask, jsonify, request, render_template
from utility_functions import generate_unique_string
from database import Livedb
from sendemail import SendEmail


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
    sendemails = SendEmail()

    send_status = sendemails.send_email(email, user_code)
    if send_status:
        message = "Email sent successfully to " + email
    else:
        message = "Error sending email to " + email
    data = {"message": message, "created": send_status, "user_status": success}
    database.close_connection()
    print(data)

    return jsonify(data)


@app.route("/db_status", methods=["GET"])
def db_status():
    data = {"status": "Active"}
    return jsonify(data)


@app.route("/user_status", methods=["POST"])
def user_status():
    database = Livedb()
    user = request.json.get("user_code")
    exists, num_keys = database.user_exist(user)
    data = {"user_status": exists}
    database.update_last_used(user)
    database.close_connection()
    return jsonify(data)


@app.route("/insert_value", methods=["POST"])
def insert_value():
    database = Livedb()

    user = request.json.get("user_code")
    key = request.json.get("key")
    value = request.json.get("value")

    if not user or not key or not value:
        return jsonify(
            {
                "message": "Error: Missing required data (user_code, key, or value)",
                "result": False,
            }
        )
    exists, num_keys = database.user_exist(user)

    if user not in db:
        db[user] = {"code": user, "data": {}}
    if len(db[user]["data"]) > num_keys and key not in db[user]["data"]:
        return jsonify(
            {
                "message": "Error: Maximum number of keys are reached. Please delete some",
                "result": False,
            }
        )

    db[user]["data"][key] = value
    database.update_last_used(user)
    database.close_connection()
    return jsonify({"result": True})


@app.route("/get_value", methods=["POST"])
def get_value():
    user_code = request.json.get("user_code")
    key = request.json.get("key")

    if not user_code or not key:
        return jsonify(
            {
                "message": "Error : Missing required data (user_code or key)",
                "result": False,
            }
        )

    if user_code not in db:
        return jsonify(
            {
                "message": "Error : Not a single value pair found",
                "result": False,
            }
        )
    user_data = db[user_code]["data"]
    value = user_data.get(key)

    if value is None:
        return jsonify(
            {"message": "Error : Key not found for the user", "result": False}
        )

    return jsonify({"result": True})


@app.route("/delete_key", methods=["POST"])
def delete_key():
    user_code = request.json.get("user_code")
    key = request.json.get("key")

    if not user_code or not key:
        return jsonify(
            {
                "message": "Error : Missing required data (user_code or key)",
                "result": False,
            }
        )

    if user_code not in db:
        return jsonify(
            {
                "message": "Error : There are no key value pairs for the user saved in DB",
                "result": False,
            }
        )

    user_data = db[user_code]["data"]

    if key not in user_data:
        return jsonify(
            {
                "message": "Key not found for the user",
                "result": False,
            }
        )
    del user_data[key]

    return jsonify(
        {
            "result": True,
        }
    )


@app.route("/delete_user_keys", methods=["POST"])
def delete_user():
    user_code = request.json.get("user_code")

    if not user_code:
        return jsonify(
            {
                "message": "Error : Missing required data (user_code)",
                "result": False,
            }
        )

    if user_code not in db:
        return jsonify(
            {
                "message": "Error : There are no key value pairs for the user saved in DB",
                "result": False,
            }
        )

    del db[user_code]  # Delete the user from the database

    return jsonify(
        {
            "result": True,
        }
    )


@app.route("/listkeyvalues", methods=["POST"])
def list_key_values():
    user_code = request.json.get("user_code")

    if not user_code:
        return jsonify(
            {
                "message": "Error : Missing required data (user_code)",
                "result": False,
            }
        )

    if user_code not in db:
        return jsonify(
            {
                "message": "Error : There are no key value pairs for the user saved in DB",
                "result": False,
            }
        )

    user_data = db.get(user_code, {}).get("data", {})
    key_value_pairs = list(user_data.items())
    if len(key_value_pairs) > 0:
        status = True
    else:
        status = False
    return jsonify({"key_value_pairs": key_value_pairs, "result": status})


if __name__ == "__main__":
    app.run(port=port)
