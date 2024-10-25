import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type


# Define the request handler class by extending BaseHTTPRequestHandler.
# This class will handle HTTP requests that the server receives.
class SimpleRequestHandler(BaseHTTPRequestHandler):

    user_list = [
            {
                'id': 1,
                'first_name': 'Michal',
                'last_name': 'Mucha',
                'role': 'Instructor'
            },
            {
                'id': 2,
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'Student'
            },
            {
                'id': 3,
                'first_name': 'Jane',
                'last_name': 'Austen',
                'role': 'Designer'
            }
        ]

    def do_OPTIONS(self):

        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(self.user_list).encode()) # WARNING: user_list hardcoded

    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        newUser = {
            'id': random.randint(1, 1000000),
            'first_name': received_data['firstName'],
            'last_name': received_data['lastName'],
            'role': received_data['role']
        }
        self.user_list.append(newUser)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(self.user_list).encode())

    def do_DELETE(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        user_id = received_data['id']
        SimpleRequestHandler.user_list = [user for user in self.user_list if user['id'] != user_id]

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(self.user_list).encode())

def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    server_address: tuple = ('', port)

    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()