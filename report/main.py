from http.server import HTTPServer
from server import Server

# Install urllib3
# Install BeautifulSoup
# Install lxml
def run(server_class = HTTPServer, handler_class = Server, port = 3004):
    server_adress = ('', port)
    print("Starting httpd server on port %d..." %port)
    httpd = server_class(server_adress, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
	run()