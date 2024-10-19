import hashlib
import secrets
from os import access

from pymongo import MongoClient

import public
from util.MongoClient import MongoIsMongoDo


# This path is provided as an example of how to use the router
def root_path(request, handler):
    mongo_client, db, chat_collection, users_collection = MongoIsMongoDo()
    with open(f"public/index.html", "rb") as file:
        html = file.read()
    visit = 0
    addcookie = ""
    html = html.decode()



    Auth=""
    account = None
    if 'Auth' in request.cookies:
        Auth = request.cookies['Auth']
        Hased_Auth = hashlib.sha256(Auth.encode()).hexdigest()
        account = users_collection.find_one({"token": Hased_Auth})

    token = ''
    if account and 'Auth' in request.cookies:
        html=html.replace("{{RegLoginSpotifyOrLogout}}", """
        <form action="/logout" method="post">
                <button type="submit">Log Out</button>
            </form>""")
        token = secrets.token_hex(32)
        users_collection.update_one({"_id": account["_id"]}, {"$set": {"xsrf_token": token}})
    else:
        html=html.replace("{{RegLoginSpotifyOrLogout}}",
        """Register:
        <form action="/register" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input type="text" name="username"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input type="password" name="password">
            </label>
            <input type="submit" value="Post">
        </form>

        Login:
        <form action="/login" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input type="text" name="username"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input type="password" name="password">
            </label>
            <input type="submit" value="Post">
        </form>
        
         <form action="/spotify-login" method="get" enctype="application/x-www-form-urlencoded">
            <input type="submit" value="Login With Spotify">
        </form>
        """)
    if 'visits' in request.cookies:
        visit = int(request.cookies["visits"]) + 1
        addcookie = f"Set-Cookie: visits={visit}; Max-Age=3600"
    else:
        visit = 1
        addcookie = f"Set-Cookie: visits={visit}; Max-Age=3600"

    html = html.replace("{{visits}}", str(visit))
    html = html.replace("{{xsrf_token}}", str(token))
    html = html.encode()

    line_len = len(html)
    # print(f"This is the Length {line_len} and this is the encoded {html_response}")
    response = "HTTP/1.1 200 OK\r\n" \
               f"Content-Length: {line_len}\r\n" \
               f"{addcookie}\r\n" \
               "X-Content-Type-Options: nosniff;\r\n" \
               "Content-Type: text/html; charset=utf-8\r\n\r\n"
    response = response.encode() + html

    handler.request.sendall(response)
