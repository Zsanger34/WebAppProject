# This path is provided as an example of how to use the router
def root_path(request, handler):
    with open("./public/index.html") as file:
        html = file.read()

    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(html)}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html}"
    handler.request.sendall(response.encode())