import util.request


class Router:

    def __init__(self):
        # Creating a routes Dict
        self.routes = []

    # This Method is used to specify how to route a specific request based on this method and path
    def add_route(self, method, path, action, exact_path=False):
        self.routes.append({"method": method, "path": path, "action": action, "exact_path": exact_path})

    # This Method takes a request which has the following
    # self.body = b""
    # self.method = ""
    # self.path = ""
    # self.http_version = ""
    # self.headers = {
    # And matches it to the routes
    def route_request(self, request, handler):
        for route in self.routes:
            if route["method"] == request.method:
                if route["exact_path"]:
                    if route["path"] == request.path:
                        route['action'](request, handler)
                        return
                else:
                    if request.path.startswith(route["path"]):
                        route['action'](request, handler)
                        return
        response_404(request, handler)

def response_404(request, handler):
    response = "HTTP/1.1 404 Not Found\r\nContent-Length: 36\r\nContent-Type: text/plain; charset=utf-8; X-Content-Type-Options: nosniff\r\n\r\nThe requested content does not exist"
    handler.request.sendall(response.encode())


def basic_add_route_False():
    router = Router()
    router.add_route("Get", "/", router.route_request, False)
    assert router.routes[0]["method"] == "Get"
    assert router.routes[0]["path"] == "/"
    assert router.routes[0]["exact_path"] == False


def basic_add_route_True():
    router = Router()
    router.add_route("Get", "/test", router.route_request, True)
    assert router.routes[0]["method"] == "Get"
    assert router.routes[0]["path"] == "/test"
    assert router.routes[0]["exact_path"] == True


if __name__ == '__main__':
    basic_add_route_False()
    basic_add_route_True()
