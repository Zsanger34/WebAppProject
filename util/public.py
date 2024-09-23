# This path is provided as an example of how to use the router
def public(request, handler):

    #We get in a route like this /public/favicon.ico
    path = request.path
    disregard, path, pfile = path.split('/')
    filep, ext = pfile.split('.')
    print(f'filep: {filep}, ext: {ext}')
    with open(f"./public/{pfile}") as file:
        html = file.read()

    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(html)}\r\nContent-Type: text/{ext}; charset=utf-8\r\n\r\n{html}"
    handler.request.sendall(response.encode())


