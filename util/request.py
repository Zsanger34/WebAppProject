class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        
        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {}
        self.cookies = {}


        #Decoding my request to a String
        request = request.decode('utf-8')
                                                                        #print(f"Start\nThis is my request: {request}")
        #Seperating the Request by the /r/n/r/n will give me the Headers and Request Line and the Body
        if "\r\n\r\n" in request:
            parsed_header, parsed_body = request.split("\r\n\r\n")
            #print(f"This is the request {request}")
        else:
            parsed_header, parsed_body = request, ""
                                                                        #print(f" This is my parsed_header {parsed_header}")
                                                                        #print(f" This is my parsed_body\n {parsed_body} \nEnd\n")
        #Seperating Headers and Request Line by seperating at the first  carriage return
        if "\r\n" in parsed_header:
            parsed_reqline, parsed_headers = parsed_header.split("\r\n", 1)
        else:
            parsed_reqline, parsed_headers = parsed_header, ""
                                                                        #print(f"This is my parsed_reqlin {parsed_reqline}")
                                                                        #print(f"This is my parsed_headers {parsed_headers}\n")
        #Parse the Request Line by splitting the whitespace
        self.method, self.path, self.http_version = parsed_reqline.split()
        #Stripping the request lines
        self.method.strip()
        self.path.strip()
        self.http_version.strip()
        #Parse the Headers by spliting the carriage returns
        headers_parsed = parsed_headers.split('\r\n')
                                                                        #print(f"This is my headers {headers_parsed}\n")
        #Looping through the headers
        for pair in headers_parsed:
            #Splitting the header by the : which seperates all values; Needs to be split at first instance due to Host  \r\nHost: localhost:8080
                                                                        #print(f'This is the pair {pair}')
            key, value = pair.split(":", 1)
            #Need to strip the whitespace from each and add into the headers
            self.headers[key.strip()] = value.strip()
            #Parsing Cookies when cookies is found same process as above for instead of colon its semi-colon
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
        self.body.strip()

       


#Basic Get Request
def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost:localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert request.path == "/"
    assert request.http_version == "HTTP/1.1"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080" # note: The leading space in the header value must be removed
    assert request.headers["Connection"] == "keep-alive"
    #print(request.headers)
    assert len(request.headers)==2
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

#Same GET request from Test 1 but adding Cookies to check for correct parsing
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

#Basic Post Request
def test_post_request():
    request = Request(b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nhello')
    assert request.method == "POST"
    assert request.path == "/path"
    assert request.http_version == "HTTP/1.1"
    assert "Content-Length" in request.headers
    assert request.headers["Content-Type"] == "text/plain"
    assert request.body == b"hello"

#GET request but with spaces to check for proper formatting
def test_headers_with_spaces():
    request = Request(b'    GET /    HTTP/1.1     \r\n    Host:   localhost:8080     \r\n    Connection:    keep-alive     \r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b"" 

#Testing basic post but without a body
def test_empty_body_POST():
    request = Request(b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\n')
    assert request.body == b""
#Testing with incorrect request
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
    
    