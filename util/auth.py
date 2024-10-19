import hashlib
import os

import bcrypt
from pymongo import MongoClient

import util.request

'''
LO1 Starts Here
'''
def extract_credentials(request):
    body = request.body.decode()
    # username=zsang&password=test Body sent when Testing the website
    body = body.split('&')
    credentials = {}
    for item in body:
        key, value = item.split('=')
        credentials[key] = value

    username = credentials['username']
    password = decode_percent_encoded(credentials['password'])

    return [username, password]


def decode_percent_encoded(password):
    i, j, decoded_password = len(password), 0, ''
    while j < i:
        if j + 2 is not i and password[j] == '%':
            decoded_password += chr(int(password[j + 1:j + 3], 16))
            j += 3
        else:
            decoded_password += password[j]
            j += 1
    return decoded_password

def validate_password(password):
    # - Minimum length of 8
    # - At least 1 lowercase letter
    lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    # - At least 1 uppercase letter
    uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
    # - At least 1 number
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # - At least 1 special character from the specified set
    specchar = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']
    if len(password) < 8:
        return False
    if not checklist(password, lowercase):
        return False
    if not checklist(password, uppercase):
        return False
    if not checklist(password, number):
        return False
    if not checklist(password, specchar):
        return False
    total = lowercase + uppercase + number + specchar
    for item in password:
        if item not in total:
            return False
    return True


def checklist(password, lst):
    for item in lst:
        if item in password:
            return True
    return False
'''
LO1 Ends here
'''
'''
LO2 Starts Here
'''
# When a user sends a registration request, store their username and a salted hash of their password in
# your database. Their password must pass the criteria tested by your validate_password method or the registration fails.

def register(request, handler):
    #mongo_client = MongoClient("mongo")
    mongo_client = MongoClient("localhost")
    db = mongo_client["cse312"]
    chat_collection = db["users"]

    username, password = extract_credentials(request)
    if validate_password(password):
        hashed_password = hash_password(password)
        chat_collection.insert_one({"username": username, "password": hashed_password, "token": ""})
    response = (
        f"HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0 \r\nLocation: /\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    )

    handler.request.sendall(response.encode())


# When a user sends a login request, authenticate the request based on the data stored in your database.
# If the [salted hash of the] password matches what you have stored in the database, the user is authenticated.

def login(request, handler):
    #mongo_client = MongoClient("mongo")
    mongo_client = MongoClient("localhost")
    db = mongo_client["cse312"]
    chat_collection = db["users"]
    real_chat_collection = db["chat"]
    username, password = extract_credentials(request)
    # hashed_password = hash_password(password)
    account = chat_collection.find_one({"username": username})
    addcookie = ""
    if account:
        db_hashed_pw = account['password']
        if bcrypt.checkpw(password.encode(), db_hashed_pw):
            token = generate_auth_token()
            token_hash = hash_token(token)
            chat_collection.update_one({"username": username}, {"$set": {"token": token_hash}})
            Auth = str(token_hash)
            addcookie = f"Set-Cookie: Auth={token_hash}; HttpOnly; Max-Age=3600\r\n"

            response = (
                f"HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0 \r\nLocation: /\r\n{addcookie}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
            )



    handler.request.sendall(response.encode())

def logout(request, handler):
    # mongo_client = MongoClient("mongo")
    mongo_client = MongoClient("localhost")
    db = mongo_client["cse312"]
    users_collection = db["users"]
    Auth = ""
    if 'Auth' in request.cookies:
        Auth = request.cookies['Auth']

    account = users_collection.find_one({"token": Auth})
    addcookie  =''
    if account:
        users_collection.update_one({"username": account["username"]}, {"$set": {"token":None}})
    else:
        addcookie = f"Set-Cookie: Auth={Auth}; MaxAge=0\r\n"


    response = (
        f"HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0 \r\nLocation: /\r\n{addcookie}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
    )
    handler.request.sendall(response.encode())
'''
Password Hashing and Checking using bcrypt
'''
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

'''
Auth Token generation and hasing
'''
def generate_auth_token():
    return os.urandom(16).hex()
def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

'''
LO2 Ends Here
'''
'''
        username=&password=
        Register:
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
        username=&password=
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
'''




'''
Below is for Testing Only
'''
def Extract_Credentials_Correct():
    request = util.request.Request(
        b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nusername=zsang&password=test')
    credentials = extract_credentials(request)
    assert credentials[0] == 'zsang'
    assert credentials[1] == 'test'


def Extract_Credentials_NoPassword():
    request = util.request.Request(
        b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nusername=zsang&password=')
    credentials = extract_credentials(request)
    assert credentials[0] == 'zsang'
    assert credentials[1] == ''


def Extract_Credentials_NoUsername():
    request = util.request.Request(
        b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nusername=&password=test')
    credentials = extract_credentials(request)
    assert credentials[0] == ''
    assert credentials[1] == 'test'


def Extract_Credentials_Complex_Password():
    request = util.request.Request(
        b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nusername=zsang&password=PAsswOrD24%21%40%23%24%25%5E%26%2C%2D%5F%3D')
    credentials = extract_credentials(request)
    assert credentials[0] == 'zsang'
    assert credentials[1] == 'PAsswOrD24!@#$%^&,-_='


def Validate_Password_Correct():
    password = 'Password1$'
    assert validate_password(password) == True


def Validate_Password_NotLongeEnough():
    password = 'Pe3$2'
    assert validate_password(password) == False


def Validate_Password_NoLowercase():
    password = 'PEREER3$2'
    assert validate_password(password) == False


def Validate_Password_NoUppercase():
    password = 'etdb24@$'
    assert validate_password(password) == False


def Validate_Password_NoNumber():
    password = 'Pe$@$@fbdb'
    assert validate_password(password) == False


def Validate_Password_NoSpecialCharacter():
    password = 'Pe33434gfdb2'
    assert validate_password(password) == False


def Validate_Password_NotSupported():
    password = 'Pe33434gf*db2'
    assert validate_password(password) == False


if __name__ == '__main__':
    Extract_Credentials_Correct()
    Extract_Credentials_NoPassword()
    Extract_Credentials_NoUsername()
    Validate_Password_Correct()
    Validate_Password_NotLongeEnough()
    Validate_Password_NoLowercase()
    Validate_Password_NoUppercase()
    Validate_Password_NoNumber()
    Validate_Password_NoSpecialCharacter()
    Validate_Password_NotSupported()
