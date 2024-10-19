# A path "/chat-messages/{id}" that accepts DELETE requests
# The {id} in the path is the id of the record to delete
# Eg. DELETE /chat-messages/1 to delete the message with id 1
# Eg. DELETE /chat-messages/2 to delete the message with id 2
# Respond with a 204 No Content response code
# There is no body to your response (We don’t want to leak information about deleted records)
# You will give the same response even if there is no message with that id or the message has already been deleted
# After this request is sent for a message, that message should never be served again (It's deleted)
# Note that the "X" next to each chat message will send a DELETE request for that message
import hashlib

from bson import ObjectId
from pymongo import MongoClient

from util.MongoClient import MongoIsMongoDo


def delete_chat(request, handler):
    mongo_client, db, chat_collection, users_collection = MongoIsMongoDo()
    path = request.path
    #Getting the ID
    disregard, path, ids = path.split('/')
    response= "HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    if 'Auth' in request.cookies:
        Auth = request.cookies['Auth']
        Hased_Auth = hashlib.sha256(Auth.encode()).hexdigest()
        account = users_collection.find_one({"token": Hased_Auth})

        if account:
            #Fixed by importing ObjectId with BSON allowed by Piazza @152
            message = chat_collection.find_one({"_id": ObjectId(ids)})
            if message and account["username"] == message["username"]:
                chat_collection.delete_one({"_id": ObjectId(ids)})
                response = (
                    f"HTTP/1.1 204 No Content\r\nX-Content-Type-Options: nosniff\r\n\r\n"
                )
        else:
            message = "Account not found or invalid credentials"
            response = (
                f"HTTP/1.1 403 Forbidden\r\nContent-Length: {len(message)}\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/plain\r\n\r\n{message}"
            )
    handler.request.sendall(response.encode())