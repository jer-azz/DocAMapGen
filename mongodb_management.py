import pymongo
from pymongo import MongoClient, GEOSPHERE

'''Get named db from MongoDB with/out authentication'''

def get_mongo_database(db_name, host='localhost', port=27017,
                       username=None, password=None):
    # Make mongo connextion with/out authentication
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s/%s' \
                    %(username, password, host, db_name)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db_name]

client = get_mongo_database('heritage_sites')
db=client.heritage_sites
coll=db.archaeo_sites
print(coll)
coll.create_index([("geometry", GEOSPHERE)])
