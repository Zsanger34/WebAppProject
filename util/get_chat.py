# This path is requested using polling to get the all the chat messages that have been sent to the app
# Respond with all of the chat history in a JSON string representing an array of objects where each object has the keys "message", "username", and "id"
# Eg. If there were two chat messages submitted saying "Hi there" and "hello", a valid response would be [{"message": "Hi there", "username": "Guest", "id": "1"}, {"message": "hello", "username": "Guest", "id": "2"}]
# The default polling in the started code is 3 seconds. You can change this value to fit your testing preferences, but make sure it's <= 3 seconds before you submit (eg. If you set it to 30 seconds, we might assume you app is broken while grading)
import json
from pymongo import MongoClient

def get_chat(request, handler):
    mongo_client = MongoClient("localhost")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]

    chat_list = []
    for chat in chat_collection.find():
        #Needed to rename to ID becuase Mongo created its own special ID if not
        chat['id'] = str(chat.pop('_id'))
        chat_list.append(chat)
    json_chat = json.dumps(chat_list)

    # Create a response
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n\r\n"
        f"{json_chat}"
    )
    handler.request.sendall(response.encode('utf-8'))