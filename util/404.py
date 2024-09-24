def response_404(request, handler):
    response = "HTTP/1.1 404 Not Found\r\nContent-Length: 36\r\nContent-Type: text/plain; charset=utf-8; X-Content-Type-Options: nosniff\r\n\r\nThe requested content does not exist"
    handler.request.sendall(response.encode())
