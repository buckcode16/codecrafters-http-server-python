import socket


def main():
    HOST = 'localhost'
    PORT = 4221
    with socket.create_server((HOST, PORT), reuse_port=True) as server_socket:
        print(f"Server is listening on {HOST},{PORT}")

        client_socket, client_address = server_socket.accept()
        print(f"Connnection from {client_address} has been established.")

        with client_socket:
            message = client_socket.recv(1024).decode("utf-8")
            print(f"Received from client: {message}")

            path = extract_path(message)
            if(path != None):
                if(path == '/'):
                    send_response(client_socket)
                else:
                    send_response(client_socket, body="Not Found", status_code=404)


def extract_path(http_request):

    lines = http_request.split('\n')

    request_line = lines[0]

    parts = request_line.split(' ')

    path = parts[1] if len(parts) > 1 else None
    return path

def send_response(client_socket, body='', content_type="text/html; charset=UTF-8", status_code=200, status_message="OK"):

    response_body = body.encode("utf-8")
    response_headers = f"HTTP/1.1 {status_code} {status_message}\r\n"\
                      f"Content-Type: {content_type}\r\n"\
                      f"Content-Length: {len(response_body)}\r\n"\
                      f"Connection: close\r\n\r\n"
    response = response_headers.encode("utf-8") + response_body

    client_socket.sendall(response)

if __name__ == "__main__":
    main()
