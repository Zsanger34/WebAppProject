class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        
        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {
            "X-Content-Type-Options": "nosniff",  # Added nosniff to preving hacking as discussed in class
        }
        self.cookies = {}

        if not request:
            return
        #Moving request to a string so i can use .split
        request = request.decode('utf-8')
        #print(f"Start\nThis is my request: {request}")
        #Seperating the Request by the /r/n/r/n will give me the Headers and Request Line and the Body
        if "\r\n\r\n" in request:

            parsed_header, parsed_body = request.split("\r\n\r\n")
            #print(f" This is my parsed_header {parsed_header}")
            #print(f" This is my parsed_body\n {parsed_body} \nEnd\n")
        else:
            parsed_header, parsed_body = request, ""
        #Seperating Headers and Request Line
        parsed_reqline, parsed_headers = parsed_header.split("\r\n", 1) 
        #Parse the Request Line
        #print(f"This is my parsed_reqlin {parsed_reqline}")
        #print(f"This is my parsed_headers {parsed_headers}\n")
        self.method, self.path, self.http_version = parsed_reqline.split()
        #Parse the Headers 
            
        headers_parsed = parsed_headers.split('\r\n')
        #print(f"This is my headers {headers_parsed}\n")
        #Had an issue with where you need to add the values into the dict can just set the output of split to it 
        for pair in headers_parsed:
            key, value = pair.split(":", 1)
            #Need to strip the whitespace from each
            self.headers[key.strip()] = value.strip()
            #Parsing Cookies
            if 'Cookie' in self.headers:
                crumbs = self.headers['Cookie'].split(";")
                for pair in crumbs:
                    key, value = pair.split("=")
                    #print(f"This is the key {key} and this is the value {value}")
                    self.cookies[key.strip()] = value.strip()
        #print(f"This is my headers {self.headers}\n")
        #print(f"This is my Cookies {self.cookies}\nEnd\n")
        #Converting Body back to Byte
        parsed_body = parsed_body.encode('utf-8')
        self.body = parsed_body
        
       


def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct
def test_withCookies():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCookie: id=X6kAwpgW29M; visits=4\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""
    assert 'id' in request.cookies
    assert request.cookies['id'] == 'X6kAwpgW29M'
    assert 'visits' in request.cookies
    assert request.cookies['visits'] == '4'

def test_post_request():
    request = Request(b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nhello')
    assert request.method == "POST"
    assert request.path == "/path"
    assert request.http_version == "HTTP/1.1"
    assert "Content-Length" in request.headers
    assert request.headers["Content-Type"] == "text/plain"
    assert request.body == b"hello"

def test_headers_with_spaces():
    request = Request(b'GET /        HTTP/1.1\r\nHost:            localhost:8080           \r\nConnection:          keep-alive         \r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b"" 

def test_empty_body_POST():
    request = Request(b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\n')
    assert request.body == b""
def test_incorrect_request():
    request = Request(b'HELP / HTTP/1.1\r\nHost: localhost\r\n\r\n')
    assert request.method == "HELP"
    assert request.path == "/"
    assert request.http_version == "HTTP/1.1"


if __name__ == '__main__':
    test1()
    test_withCookies()
    test_post_request()
    test_headers_with_spaces()
    test_empty_body_POST()
    test_incorrect_request()
    
    