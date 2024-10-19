from datetime import datetime
from flask import Flask, jsonify, render_template, request
from redis import Redis
from flask_cors import CORS
from helpers import update_feature_to_db,create_new_table,insert_feature_to_db, has_feature_been_deleted, convert_enabled_value  # Import the helper functions
import sqlite3

insert_query = '''
INSERT INTO "flag" (name, description, roll_out, enabled, deleted, deleted_at, created_at, updated_at)
VALUES ( ?, ?, ?, ?, ?, ?, ?, ?);
'''
db = "feature_flag.db"

create_new_table(db)

def does_have_key(pattern):
    for _ in redis.scan_iter(match=pattern):
        return True
    return False

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

@app.route("/features", methods=["POST"])
def feature():
    json = request.get_json()
    title = json["title"]
    description= json["description"]
    roll_out = json["roll_out"]
    enabled = convert_enabled_value(json)
    
    insert_feature_to_db(db, title,description,enabled,roll_out)
    return "Feature Created"

@app.route("/feature/<id>", methods=["GET"])
def get_feature(id):
    redis_key =f"feature:{id}"
    feature_data = redis.hgetall(redis_key)
    if feature_data:
        if has_feature_been_deleted(feature_data):
             return jsonify({"error": f"Feature '{id}' not found"}), 404
        return jsonify({"name":id, "data":feature_data}), 200
    else:
        return jsonify({"error": f"Feature '{id}' not found"}), 404
  
@app.route("/features", methods=["GET"])
def get_all_features():
    features = {}
    if(does_have_key("feature:*") == False): 
        return features
    for key in redis.scan_iter(match="feature:*"):
      
        feature_data = redis.hgetall(key)
        print(has_feature_been_deleted(feature_data))
        if(has_feature_been_deleted(feature_data) == False):
            features[key] = feature_data
    return features

@app.route("/feature/<id>", methods=["PUT"])
def update_feature(id):
    #We need to update the databse to match the changes made
    redis_key =f"feature:{id}"
    if not redis.exists(redis_key):
        return jsonify({"error": f"Feature '{id}' not found"}), 404
    
    update_data = request.get_json()
    if update_data['updateData']:
        update_data=update_data['updateData']
        if(update_data['enabled'] == 'True'):
            update_data['enabled']=True
        else:
            update_data['enabled']=False
   

    if not update_data:
        return jsonify({"error": "No fields provided for update"}), 400
    
    update_data['enabled']= convert_enabled_value(update_data)
    update_data["updated_at"] = int(datetime.now().timestamp())
    update_feature_to_db(db, update_data)
    redis.hset(redis_key, mapping=update_data)
    return jsonify({"message": f"Feature updated successfully", "updated_fields": update_data}), 200

@app.route("/feature/<id>", methods=["DELETE"])
def delete_feature(id):
    #We need to update the databse to match the changes made
    redis_key =f"feature:{id}"
    can_not_delete_key= not redis.exists(redis_key) or int(redis.hget(redis_key,'deleted')) == 1
    feature_name = redis.hget(redis_key, 'title')

    if can_not_delete_key:
        return jsonify({"error": f"Feature '{feature_name}' not found"}), 404

    redis.hset(redis_key,mapping={
        'deleted': 1,
        'deleted_at': int(datetime.now().timestamp())
    })
    return jsonify({"message": f"Feature '{feature_name}' deleted successfully"}), 200

@app.route("/count", methods=["GET"])
def count():
    print("yey running")
    response = {"count": 1}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
