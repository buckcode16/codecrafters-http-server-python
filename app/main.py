# Uncomment this to pass the first stage
import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()
    print(f"Connnection from {client_address} has been established.")

    message = client_socket.recv(1024).decode("utf-8")
    print(f"Received from client: {message}")

    client_socket.sendall("HTTP/1.1 200\r\n\r\n".encode("utf-8"))


if __name__ == "__main__":
    main()
