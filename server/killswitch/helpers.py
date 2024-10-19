# helpers.py
import sqlite3
from datetime import datetime
from redis import Redis
insert_query = '''
INSERT INTO "flag" (name, description,enabled,roll_out, deleted, deleted_at, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
'''

redis = Redis(host="127.0.0.1", port=6379,decode_responses=True)

def has_feature_been_deleted(feature):
    """
    Check if a feature has been deleted based on the 'deleted' field in the feature hash.
    Returns True if the feature has been marked as deleted.
    """
    return int(feature['deleted']) == 1   

def convert_enabled_value(feature):
    """
    Convert the 'enabled' value in the feature hash to an integer (1 or 0).
    Returns 1 if the feature is enabled, otherwise returns 0.
    """
    return 1 if feature['enabled'] is True else 0

def create_new_table(db, should_drop=False, should_insert_test_data=False):
    """
    Creates a new table if needed.
    """

    con = sqlite3.connect(db)
    cur = con.cursor()
    if(should_drop):
        con.execute("DROP TABLE flag") 
        redis.flushdb()
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
    
    if(should_insert_test_data):
        insert_test_data(db)

def insert_test_data(db):
    insert_feature_to_db(db,'New Feature','This feature enables X.',True,75)

def add_feature_to_redis(db, feature):
    id = None
    title=feature['title']
    description=feature['description']
    enabled=feature['enabled']
    roll_out=feature['roll_out']
    with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f'''
            SELECT id 
            FROM flag
            WHERE name = '{title}'
            ''')
            result = cur.fetchone()
            if result:
                id = result[0]
                print(f"ID for feature '{title}': {id}")
            else:
                print(f"No feature found with name '{title}'")
    redis_key = f"feature:{id}"
        
       
    redis.hset(redis_key, mapping= {
        "id": id,
        "title": title,
        "description": description,
        "enabled": enabled,
        "roll_out": roll_out,
        "deleted": 0,
        "deleted_at": 0,
        "created_at": int(datetime.now().timestamp()),
        "updated_at": int(datetime.now().timestamp())
    })
    
def update_feature_to_db(db,feature):
    print('feature:',feature)
    with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f'''
                        UPDATE flag
                        SET name = '{feature['title']}',
                        description = '{feature['description']}',
                        enabled = '{feature['enabled']}',
                        roll_out = '{feature['roll_out']}',
                        updated_at= '{feature['updated_at']}'
                        WHERE id = {int(feature['id'])};
            ''')
            result = cur.fetchone()
            if result:
                print("result:", result)


    
def insert_feature_to_db(db, title,description,enabled,roll_out):
    """
    Adds the feature into the database and adds the feature to redis
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    data_to_insert = {
    "title": title,
    "description": description,
    "enabled":  enabled,
    "roll_out": roll_out,
    "deleted": 0,
    "deleted_at": 0,
    "created_at": int(datetime.now().timestamp()),
    "updated_at": int(datetime.now().timestamp())
    }

    print(data_to_insert)
    data_to_insert['enabled'] = convert_enabled_value(data_to_insert)
   
    feature = (
        data_to_insert["title"], 
        data_to_insert["description"],
        data_to_insert["enabled"],
        data_to_insert['roll_out'],
        data_to_insert['deleted'],
        data_to_insert['deleted_at'],
        data_to_insert['created_at'],
        data_to_insert['updated_at']
        )
    print(feature)
    
    cur.execute(insert_query, feature)
    con.commit()
    con.close()

    add_feature_to_redis(db,data_to_insert)

    return "Feature Created"