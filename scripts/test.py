import http.server
import socket
import socketserver
import os

PORT = 8000
SITE_DIR = "site"
STATIC_DIR = "static"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split("?")[0]

        if path == "/":
            full_path = os.path.join(os.getcwd(), SITE_DIR, "index.html")
        elif path.startswith("/static/"):
            rel_path = path[len("/static/") :]
            full_path = os.path.join(os.getcwd(), STATIC_DIR, rel_path)
        else:
            rel_path = path.lstrip("/")
            full_path = os.path.join(os.getcwd(), SITE_DIR, rel_path)

            if os.path.exists(full_path + ".html"):
                full_path += ".html"

        return full_path

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            self.send_response(404, message)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            with open(os.path.join(os.getcwd(), SITE_DIR, "404.html"), "rb") as f:
                self.wfile.write(f.read())
        else:
            super().send_error(code, message, explain)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 1))

    return s.getsockname()[0]


def run(server_class=http.server.HTTPServer, handler_class=CustomHandler):
    local_ip = get_local_ip()

    print(f"Serving at http://{local_ip}:{PORT}")

    with ReusableTCPServer(("", PORT), handler_class) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer shut down!")


if __name__ == "__main__":
    run()
