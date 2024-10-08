import public


# This path is provided as an example of how to use the router
def root_path(request, handler):
    with open(f"public/index.html", "rb") as file:
        html = file.read()
    visit = 0
    addcookie = ""
    html = html.decode()
    if 'visits' in request.cookies:
        visit = int(request.cookies["visits"]) + 1
        addcookie = f"Set-Cookie: visits={visit}; Max-Age=3600"
    else:
        visit = 1
        addcookie = f"Set-Cookie: visits={visit}; Max-Age=3600"

    html = html.replace("{{visits}}", str(visit))
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
