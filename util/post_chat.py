# This path is used when a user types a chat message and clicks send
# The front end will send these chat messages in a JSON string with the format:
# {"message": "The message being sent"}
# You are allowed to use Python's json module to parse and format your JSON strings
# When you receive a chat message, you will store it in your database with:
# The message that was sent, the username of the user that sent the message (You can use "Guest" for now), and a unique id for the message
# You may choose what you send in response to these requests (The front end will ignore the response)
import json
import html
from pymongo import MongoClient


def post_chat(request, handler):
    mongo_client = MongoClient("localhost")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]

    jbody = json.loads(request.body.decode())
    body = jbody.get('message', '')

    msg_id = chat_collection.count_documents({})
    if msg_id is None:
        msg_id = 0
        print("It was none")

    addcookie = ""
    # UserID = ""
    # if 'UserID' in request.cookies:
    #     UserID = request.cookies['UserID']
    # else:
    #     UserID = str(msg_id)
    #     addcookie = f"Set-Cookie: UserID={msg_id}\r\n"

    chat_collection.insert_one({"_id": str(msg_id), "username": "GUEST", "message": html.escape(body), "UserID": f"{UserID}"})

    response_msg = "Message has been sent"

    response = (
        f"HTTP/1.1 201 Created\r\nContent-Length: {len(response_msg)}\r\n{addcookie}Content-Type: application/json\r\n\r\n{response_msg}"
    )
    handler.request.sendall(response.encode())
