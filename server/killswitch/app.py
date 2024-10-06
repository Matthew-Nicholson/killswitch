from datetime import datetime
from flask import Flask, jsonify, render_template, request
from redis import Redis
from flask_cors import CORS
import sqlite3

db = "feature_flag.db"
con = sqlite3.connect(db)
cur = con.cursor()
create_table_query = '''
CREATE TABLE "flag" (
    "id" INTEGER NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "roll_out" INTEGER,
    "deleted" INTEGER,
    "deleted_at" INTEGER NOT NULL,
    "created_at" INTEGER NOT NULL,
    "updated_at" INTEGER NOT NULL,
    PRIMARY KEY("id"),
    CHECK("roll_out" <= 100 AND "roll_out" >= 0),
    CHECK("deleted" <= 1 AND "deleted" >= 0)
);
'''
# cur.execute(create_table_query)
# con.commit()  # Commit to ensure the table is created

insert_query = '''
INSERT INTO "flag" (id, name, description, roll_out, deleted, deleted_at, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
'''
data_to_insert = (1, 'New Feature', 'This feature enables X.', 75, 0, 0, int(datetime.now().timestamp()), int(datetime.now().timestamp()))

# cur.execute(insert_query, data_to_insert)
# con.commit()

# Close the connection
con.close()

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
    response = {"count": 1}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
