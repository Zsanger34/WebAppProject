# This path is used when a user types a chat message and clicks send
# The front end will send these chat messages in a JSON string with the format:
# {"message": "The message being sent"}
# You are allowed to use Python's json module to parse and format your JSON strings
# When you receive a chat message, you will store it in your database with:
# The message that was sent, the username of the user that sent the message (You can use "Guest" for now), and a unique id for the message
# You may choose what you send in response to these requests (The front end will ignore the response)
import json
def post_chat(request, handler):
    pass