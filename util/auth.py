import util.request


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
