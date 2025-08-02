import http.server
import socketserver
import os

PORT = 8000
SITE_DIR = "site"
STATIC_DIR = "static"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path == "/":
            full_path = os.path.join(os.getcwd(), SITE_DIR, "index.html")
        elif path.startswith("/static/"):
            rel_path = path[len("/static/") :]
            full_path = os.path.join(os.getcwd(), STATIC_DIR, rel_path)
        else:
            rel_path = path.lstrip("/")
            full_path = os.path.join(os.getcwd(), SITE_DIR, rel_path) + ".html"

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


def run(server_class=http.server.HTTPServer, handler_class=CustomHandler):
    print(f"Serving at http://localhost:{PORT}")

    with ReusableTCPServer(("", PORT), handler_class) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    run()
