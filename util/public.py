# This path is provided as an example of how to use the router
# TODO When people look up http://localhost:8080/public/image/ It needs to return a 404 so I need to make a 404 class and have it route
def public(request, handler):
    mime = {
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "ico": "image/x-icon",
        "png": "image/png",
        "jpg": "image/jpg",
        "jpeg": "image/jpeg",
    }

    #We get in a route like this /public/favicon.ico
    path = request.path #This will containg the path /public/favicon.ico
    if 'image' in path:
        disregard, path, spath, pfile = path.split('/')
        #print(f"Thios is the file {pfile}")
        filep, ext = pfile.split('.')  # This will split at . with the following filep = "favicon" ext ="ico"
        # print(f'filep: {filep}, ext: {ext}')
        #print(f"./public/image/{pfile} Bruh {mime[ext]}")
        with open(f"./public/image/{pfile}", "rb") as file:
            html = file.read()

        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(html)}\r\nX-Content-Type-Options: nosniff; \r\nContent-Type:image\jpg;\r\n\r\n"
        response = response.encode() + html

        handler.request.sendall(response)
    else:
        disregard, path, pfile = path.split('/')  # this will split at / with the follow disreagard = "" path ="favicon.ico"

        filep, ext = pfile.split('.') #This will split at . with the following filep = "favicon" ext ="ico"
        #print(f'filep: {filep}, ext: {ext}')
        if ext == "ico":
            with open(f"./public/{pfile}", "rb") as file:
                html = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(html)}\r\nX-Content-Type-Options: nosniff; Content-Type: {mime[ext]}; charset=utf-8\r\n\r\n{html}"
            handler.request.sendall(response.encode())
        else:
            with open(f"./public/{pfile}", "r") as file:
                html = file.read()
            #print(f"Hopeflly we are still grabbing the css ./public/{pfile}")
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(html)}\r\nX-Content-Type-Options: nosniff; Content-Type: {mime[ext]}; charset=utf-8\r\n\r\n{html}"
            handler.request.sendall(response.encode())




