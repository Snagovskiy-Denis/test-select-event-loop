import socket

from event_loop import loop, create_task


HOST, PORT = "127.0.0.1", 8000


def handle_request(sock: socket.socket, addr: str):
    print(f"Connection from -> {addr}")

    with sock:
        yield sock
        request = sock.recv(1024)
        print(f"Received -> {request}")
        request = b"pong" if request == b"ping" else request
        sock.send(request.upper())

    print(f"Connection is ended <- {addr}")


def start_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv_sock:
        srv_sock.bind((host, port))
        srv_sock.setblocking(False)
        srv_sock.listen(1)

        print(f"Starting server at {host}:{port}")

        while True:
            yield srv_sock
            client_sock, addr = srv_sock.accept()
            client_sock.setblocking(False)
            # yield from handle_request(client_sock, addr)  # await
            create_task(handle_request(client_sock, addr))  # schedule


if __name__ == "__main__":
    loop(start_server(HOST, PORT))
