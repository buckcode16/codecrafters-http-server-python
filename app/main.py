import socket

def main():
    HOST = 'localhost'
    PORT = 4221
    while True:
        print(f"Server is listening on {HOST},{PORT}")

        with socket.create_server((HOST, PORT), reuse_port=True) as server_socket:
            client_socket, client_address = server_socket.accept()
            print(f"Connnection from {client_address} has been established.")

            with client_socket:
                message = client_socket.recv(1024).decode("utf-8")
                print(f"Received from client: {message}")

                path = extract_path(message)

                if(path == '/' or path.startswith('/echo/')):
                    send_response(client_socket,path)
                else:
                    send_response(client_socket,path, status_code = 404)


def extract_path(http_request):

    lines = http_request.split('\n')

    request_line = lines[0]

    parts = request_line.split(' ')

    path = parts[1] if len(parts) > 1 else None
    
    return path

def extract_last_string(http_request):

    lines = http_request.split('\n')

    request_line = lines[0]

    parts = request_line.split(' ')

    path = parts[1] if len(parts) > 1 else None
    
    random_string = path.split('/')

    extract = random_string[-1] if len(random_string) > 1 else None
    return extract

def send_response(client_socket, path, status_code = 200):

    content_type = "text/html; charset=UTF-8"
    body = ''
    status_message = "OK"

    if path.startswith('/echo/'):
        content_type = "text/plain"
        body = path[len('/echo/'):]
    
    if (status_code == 404):
        status_message = "Not Found"

    response_body = body.encode("utf-8")
    content_length = len(response_body)

    response_headers = f"HTTP/1.1 {status_code} {status_message}\r\n"\
                      f"Content-Type: {content_type}\r\n"\
                      f"Content-Length: {content_length}\r\n\r\n"
    response = response_headers.encode("utf-8") + response_body

    client_socket.sendall(response)

if __name__ == "__main__":
    main()
