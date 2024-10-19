import base64
import os
import requests
from urllib3 import request

from util.MongoClient import MongoIsMongoDo
from util.auth import generate_auth_token, hash_token

'''
Requesting Authorization to access data
'''

def spotify_login(request, handler):
    client_id = os.getenv("client_id")
    redirect_uri = os.getenv("redirect_uri")

    '''
    Needed Parameters are
    client_id
    response_type
    redirect_uri
    scope

    We do not need state
    '''

    redirect_url = (f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=user-read-email")
    response = (
        f"HTTP/1.1 302 Found\r\nLocation: {redirect_url}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    )
    handler.request.sendall(response.encode())

def spotify_return(request, handler):
    mongo_client, db, chat_collection, users_collection = MongoIsMongoDo()
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    redirect_uri = os.getenv("redirect_uri")

    path = request.path
    print(path)
    #/spotify?code = AQDNs
    disregard, code = path.split("=", 1)
    print(f"THis is the code {code}")
    response =''
    if not code:
        response = f"HTTP/1.1 404 Bad Request\r\nContent-Length:0\r\n\r\n"
    else:
    # If the user accepted your request, then your app is ready to exchange
    # the authorization code for an access token. It can do this by sending a POST request to the /api/token endpoint.
        '''
        Requesting access and refresh tokens
        '''
        token_url = "https://accounts.spotify.com/api/token"
        Body_Params={"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri}
        auth_str = f"{client_id}:{client_secret}"
        auth_bytes = base64.b64encode(auth_str.encode()).decode()

        Header_Params={"Authorization": f"Basic {auth_bytes}","Content-Type": "application/x-www-form-urlencoded"}

        token_response = requests.post(token_url, headers=Header_Params, data=Body_Params)

        print(f"This is the token {token_response.text}")
        if token_response.status_code == 200:
            #Will return a JSON String with access_token, token_type, scope, expires_in, refresh_token
            token_data = token_response.json()
            access_token = token_data.get('access_token')
            profile_data = requests.get("https://api.spotify.com/v1/me",headers={"Authorization": f"Bearer {access_token}"}).json()

            SUserID = profile_data['id']
            email = profile_data['email']

            user = users_collection.find_one({"SUserID": SUserID})
            token = generate_auth_token()
            token_hash = hash_token(token)
            if user:
                users_collection.update_one({"SUserID": SUserID}, {"$set": {"token": token_hash}})
            else:
                users_collection.insert_one({"SUserID":SUserID, "username": email,"token": f"{token_hash}"})

            addcookie = f"Set-Cookie: Auth={token}; HttpOnly; Max-Age=3600\r\n"
            response = f"HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0 \r\nLocation: /\r\n{addcookie}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
        else:
            response = f"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    handler.request.sendall(response.encode())