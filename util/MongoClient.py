from pymongo import MongoClient

def MongoIsMongoDo():
    mongo_client = MongoClient("mongo")
    #mongo_client = MongoClient("localhost")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]
    users_collection = db["users"]

    #mongo_client, db, chat_collection. users_collection = MongoIsMongoDo()
    return [mongo_client, db, chat_collection, users_collection]