import socket
import time
import os

def start_proxy():
    # Use environment variables or defaults
    proxy_host = "0.0.0.0"
    proxy_port = int(os.environ.get("PORT", 8080))

    # Hardcode or use env vars for destination
    dest_host = os.environ.get("DEST_HOST", "example.com")
    dest_port = int(os.environ.get("DEST_PORT", 80))

    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.bind((proxy_host, proxy_port))
    proxy_server.listen(1)
    print(f'Proxy server listening on {proxy_host}:{proxy_port}...')
    print(f'Forwarding to destination {dest_host}:{dest_port}...')

    while True:
        try:
            client_socket, client_address = proxy_server.accept()
            print(f'Received connection from {client_address}')

            dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dest_socket.connect((dest_host, dest_port))
            print(f'Connected to destination server {dest_host}:{dest_port}')

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                dest_socket.sendall(data)
                data = dest_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)

            client_socket.close()
            dest_socket.close()
        except Exception as e:
            print(f'Error: {e}. Retrying in 5 seconds...')
            time.sleep(5)

if __name__ == '__main__':
    start_proxy()
