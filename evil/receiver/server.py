from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = self.rfile.read(content_length).decode('utf-8')

        print(f"[INFO] Received string: {payload}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"String received successfully")


def main(server_class=HTTPServer, handler_class=RequestHandler, port=8001):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"[INFO] Starting HTTP server on port {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    main()
