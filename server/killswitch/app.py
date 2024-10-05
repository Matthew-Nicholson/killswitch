from flask import Flask, jsonify, render_template, request
from redis import Redis
from flask_cors import CORS


app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:5173",
        },
    },
)
redis = Redis(host="127.0.0.1", port=6379)
try:
    ping = redis.ping()
    redis.set("planet", "World!")
except Exception:
    print("Redis is not running")
    exit(1)


@app.route("/", methods=["GET"])
def index():
    planet = request.args.get("planet")
    if planet:
        redis.set("planet", planet)
    return render_template("index.html", planet=redis.get("planet").decode("utf-8"))


@app.route("/features", methods=["POST"])
def feature():
    json = request.get_json()
    print(json)
    name = json["name"]
    enabled = json["enabled"]
    redis.set(name, enabled)
    return "OK"


@app.route("/features", methods=["GET"])
def features():
    features = {}
    for key in redis.scan_iter(match="feature:*"):
        features[key.decode("utf-8")] = redis.get(key).decode("utf-8")
    return features


@app.route("/count", methods=["GET"])
def count():
    print("yey running")
    response = {"count": 69420}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
