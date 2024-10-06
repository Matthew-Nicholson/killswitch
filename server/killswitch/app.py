from datetime import datetime
from flask import Flask, jsonify, render_template, request
from redis import Redis
from flask_cors import CORS
import sqlite3

db = "feature_flag.db"
con = sqlite3.connect(db)
cur = con.cursor()

# con.execute("DROP TABLE flag") 

create_table_query = '''
CREATE TABLE  IF NOT EXISTS "flag" (
    "id" INTEGER NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "enabled" INTEGER,
    "roll_out" INTEGER,
    "deleted" INTEGER,
    "deleted_at" INTEGER,
    "created_at" INTEGER NOT NULL,
    "updated_at" INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT),
    CHECK("roll_out" <= 100 AND "roll_out" >= 0),
    CHECK("deleted" <= 1 AND "deleted" >= 0)
);
'''
cur.execute(create_table_query)

insert_query = '''
INSERT INTO "flag" (name, description, roll_out, enabled, deleted, deleted_at, created_at, updated_at)
VALUES ( ?, ?, ?, ?, ?, ?, ?, ?);
'''
# data_to_insert = ('New Feature', 'This feature enables X.', 75, 1, 0,0, int(datetime.now().timestamp()), int(datetime.now().timestamp()))
# cur.execute(insert_query, data_to_insert)
con.commit()
con.close()

def insert_feature_to_db(name,description,roll_out, enabled):
    global db
    global insert_query
    con = sqlite3.connect(db)
    cur = con.cursor()
    data_to_insert = (name, description, roll_out, enabled, 0,0, int(datetime.now().timestamp()), int(datetime.now().timestamp()))
    cur.execute(insert_query, data_to_insert)
    con.commit()
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
redis = Redis(host="127.0.0.1", port=6379,decode_responses=True)
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

def has_feature_been_deleted(feature):
    return int(feature['deleted']) == 1   

def convert_enabled_value(feature):
    return 1 if feature['enabled']is True else 0


@app.route("/features", methods=["POST"])
def feature():
    json = request.get_json()
    name = json["name"]
    description= json["description"]
    roll_out = json["roll_out"]
    enabled = convert_enabled_value(json)

    redis_key = f"feature:{name}"
    if redis.exists(redis_key):
        return f"Feature '{name}' already exists. Choose a different name."
    
    insert_feature_to_db(name,description,roll_out,enabled)
    redis.hset(redis_key, mapping= {
        "enabled": enabled,
        "description": description,
        "roll_out": roll_out,
        "deleted": 0,
        "deleted_at": 0,
        "created_at": int(datetime.now().timestamp()),
        "updated_at": int(datetime.now().timestamp())
    })
    
    return "Feature Created"

@app.route("/feature/<name>", methods=["GET"])
def get_feature(name):
    redis_key =f"feature:{name}"
    feature_data = redis.hgetall(redis_key)
    if feature_data:
        if has_feature_been_deleted(feature_data):
             return jsonify({"error": f"Feature '{name}' not found"}), 404
        return jsonify({"name":name, "data":feature_data}), 200
    else:
        return jsonify({"error": f"Feature '{name}' not found"}), 404
  
@app.route("/features", methods=["GET"])
def get_all_features():
    features = {}
    for key in redis.scan_iter(match="feature:*"):
        feature_data = redis.hgetall(key)
        if(has_feature_been_deleted(feature_data) == False):
            features[key] = feature_data
    return features

@app.route("/feature/<name>", methods=["PUT"])
def update_feature(name):
    redis_key =f"feature:{name}"
    if not redis.exists(redis_key):
        return jsonify({"error": f"Feature '{name}' not found"}), 404
    
    update_data = request.get_json()

    if not update_data:
        return jsonify({"error": "No fields provided for update"}), 400
    
    update_data['enabled'] = 0 if update_data['enabled']== False else 1

    redis.hset(redis_key, mapping=update_data)
    redis.hset(redis_key, "updated_at", int(datetime.now().timestamp()))
    return jsonify({"message": f"Feature '{name}' updated successfully", "updated_fields": update_data}), 200

@app.route("/feature/<name>", methods=["DELETE"])
def delete_feature(name):
    redis_key =f"feature:{name}"
    can_not_delete_key= not redis.exists(redis_key) or int(redis.hget(redis_key,'deleted')) == 1

    if can_not_delete_key:
        return jsonify({"error": f"Feature '{name}' not found"}), 404

    redis.hset(redis_key,mapping={
        'deleted': 1,
        'deleted_at': int(datetime.now().timestamp())
    })
    return jsonify({"message": f"Feature '{name}' deleted successfully"}), 200




@app.route("/count", methods=["GET"])
def count():
    print("yey running")
    response = {"count": 1}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
