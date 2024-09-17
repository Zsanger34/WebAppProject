class Router:

    def __init__(self):
        #Creating a routes Dict
        self.routes = []

    #This Method is used to specify how to route a specific request based on tis method and path
    def add_route(self, method, path, action, exact_path=False):
        self.routes.append({"method": method,"path": path, "action":action, "exact_path": exact_path})

    #This Method takes a request which has the following
    # self.body = b""
    # self.method = ""
    # self.path = ""
    # self.http_version = ""
    # self.headers = {
    #And matches it to the routes 
    def route_request(self, request, handler):
        pass

def test1():
    router = Router()
    router.add_route("Get", "/", route_request, False)
    assert route.routes[0]["method"] == "Gete"
