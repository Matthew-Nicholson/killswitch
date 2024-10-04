from flask import Flask, render_template, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='127.0.0.1', port=6379)
try:
    ping = redis.ping()
    redis.set('planet', 'World!')
except Exception:
    print('Redis is not running')
    exit(1)

@app.route('/')
def index():
    return render_template('index.html', planet=redis.get('planet').decode('utf-8'))

@app.route('/features', methods=['POST'])
def feature():
    json = request.get_json()
    print(json)
    name = json['name']
    enabled = json['enabled']
    redis.set(name, enabled)
    return 'OK'

@app.route('/features', methods=['GET'])
def features():
    features = {}
    for key in redis.scan_iter(match='feature:*'):
        features[key.decode('utf-8')] = redis.get(key).decode('utf-8')
    return features

if __name__ == '__main__':
    app.run(debug=True, port=5001)
