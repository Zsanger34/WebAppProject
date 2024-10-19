# This path is used when a user types a chat message and clicks send
# The front end will send these chat messages in a JSON string with the format:
# {"message": "The message being sent"}
# You are allowed to use Python's json module to parse and format your JSON strings
# When you receive a chat message, you will store it in your database with:
# The message that was sent, the username of the user that sent the message (You can use "Guest" for now), and a unique id for the message
# You may choose what you send in response to these requests (The front end will ignore the response)
import hashlib
import json
import html
import os

from pymongo import MongoClient

from util.MongoClient import MongoIsMongoDo


def post_chat(request, handler):
    mongo_client, db, chat_collection, users_collection = MongoIsMongoDo()
    jbody = json.loads(request.body.decode())
    body = jbody.get('message', '')


    # msg_id = chat_collection.count_documents({})
    # if msg_id is None:
    #     msg_id = 0
    #     print("It was none")
    response_msg = f"Message has been sent"


    addcookie = ""
    UserID = ""
    username = "GUEST"
    if 'UserID' in request.cookies:
        UserID = request.cookies['UserID']
    else:
        UserID = os.urandom(16).hex()
        addcookie = f"Set-Cookie: UserID={UserID}\r\n"
    response = (
        f"HTTP/1.1 201 Created\r\nContent-Length: {len(response_msg)}\r\nX-Content-Type-Options: nosniff\r\n{addcookie}Content-Type: application/json\r\n\r\n{response_msg}"
    )
    if 'Auth' in request.cookies:
        Auth = request.cookies['Auth']
        Hased_Auth = hashlib.sha256(Auth.encode()).hexdigest()
        account = users_collection.find_one({"token": Hased_Auth})

        if account:
            username = str(account['username'])
            xsrf_token = request.headers.get("X-XSRF-TOKEN", None)
            db_token = account["xsrf_token"]
            if xsrf_token and account["xsrf_token"] == xsrf_token:
                chat_collection.insert_one({"username": username, "message": html.escape(body), "UserID": f"{UserID}"})
            else:
                message =f"This XSRF token was not issued to this user"
                response = f"HTTP/1.1 403 Forbidden\r\nContent-Length: {len(message)}\r\nX-Content-Type-Options: nosniff\r\n\r\n{message}"
        else:
            chat_collection.insert_one({"username": username, "message": html.escape(body), "UserID": f"{UserID}"})

    else:
        chat_collection.insert_one({"username": username, "message": html.escape(body), "UserID": f"{UserID}"})



    handler.request.sendall(response.encode())
