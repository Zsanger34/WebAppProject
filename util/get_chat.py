# This path is requested using polling to get the all the chat messages that have been sent to the app
# Respond with all of the chat history in a JSON string representing an array of objects where each object has the keys "message", "username", and "id"
# Eg. If there were two chat messages submitted saying "Hi there" and "hello", a valid response would be [{"message": "Hi there", "username": "Guest", "id": "1"}, {"message": "hello", "username": "Guest", "id": "2"}]
# The default polling in the started code is 3 seconds. You can change this value to fit your testing preferences, but make sure it's <= 3 seconds before you submit (eg. If you set it to 30 seconds, we might assume you app is broken while grading)
import json
from pymongo import MongoClient

from util.MongoClient import MongoIsMongoDo


def get_chat(request, handler):
    mongo_client, db, chat_collection, users_collection = MongoIsMongoDo()


    chat_list = []
    for chat in chat_collection.find():
        #renamed to ID becuase Mongo created its own special ID if not everything gets weird
        #I dont know why I was changing this to a id instead of _is
        #Zac Again Dont ever change that line ever
        #Time Wasted: 1 hour
        chat['id'] = str(chat.pop('_id'))
        chat_list.append(chat)

    if 'UserID' in request.cookies:
        UserID = request.cookies['UserID']
    else:
        UserID = 'None'
    Id_and_Chat = {
        "chats": chat_list,
        "UserID": UserID
    }
    json_chat = json.dumps(Id_and_Chat)

    # Create a response
    response = (
        "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\n\r\n"
        f"{json_chat}"
    )
    handler.request.sendall(response.encode('utf-8'))