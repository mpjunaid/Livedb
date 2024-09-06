from flask import Flask, jsonify

port = 5000  # Global parameter

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to the Livedb server"


@app.route("/db")
def get_data():
    data = {"key": "tst_value"}
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=port)
