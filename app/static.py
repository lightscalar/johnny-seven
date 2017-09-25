import http.server
import socketserver
import os

# Serve static index.html file from the /site directory.
PORT = 5000

if __name__ == '__main__':

    # Switch into appropriate directory.
    web_dir = os.path.join(os.path.dirname(__file__), '../dist')
    os.chdir(web_dir)

    # Launch web server.
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("Launching Static Server on Port", PORT)
    httpd.serve_forever()
