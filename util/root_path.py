import public
# This path is provided as an example of how to use the router
def root_path(request, handler):
    html = open("public/index.html", "r")
    for line in html:
        line.encode()
        line_len = len(line)
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {line_len}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{line}"
        handler.request.sendall(response.encode())
