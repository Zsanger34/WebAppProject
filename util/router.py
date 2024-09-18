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
                else:
                    routeLen = len(route["path"])
                    if request.path[:routeLen] == request.path:
                        route['action'](request, handler)
        response_404(request, handler)


def response_404(request, handler):
    response = "HTTP/1.1 404 Not Found\r\nContent-Length: 36\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nThe requested content does not exist"
    handler.request.sendall(response.encode())

def test1():
    router = Router()
    router.add_route("Get", "/", router.route_request, False)
    assert router.routes[0]["method"] == "Get"


if __name__ == '__main__':
    test1()
