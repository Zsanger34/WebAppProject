# A path "/chat-messages/{id}" that accepts DELETE requests
# The {id} in the path is the id of the record to delete
# Eg. DELETE /chat-messages/1 to delete the message with id 1
# Eg. DELETE /chat-messages/2 to delete the message with id 2
# Respond with a 204 No Content response code
# There is no body to your response (We don’t want to leak information about deleted records)
# You will give the same response even if there is no message with that id or the message has already been deleted
# After this request is sent for a message, that message should never be served again (It's deleted)
# Note that the "X" next to each chat message will send a DELETE request for that message
from pymongo import MongoClient
def delete_chat(request, handler):
    #mongo_client = MongoClient("mongo")
    mongo_client = MongoClient("localhost")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]
    path = request.path
    #Getting the ID
    disregard, path, ids = path.split('/')
    chat_collection.delete_one({"_id": str(ids)})
    auth=''
    if 'auth' in request.cookies:
        auth = request.cookies['auth']
    else:
        auth = str(auth)
        addcookie = f"Set-Cookie: auth={auth}\r\n"

    response = (
        f"HTTP/1.1 204 No Content\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    )
    handler.request.sendall(response.encode())