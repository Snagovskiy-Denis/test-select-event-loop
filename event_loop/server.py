import socket
import random

from event_loop import loop, create_task, read_ready, sleep


HOST, PORT = "127.0.0.1", 8000
SIMULATE_SLOW_IO = True


def handle_request(sock: socket.socket, addr: str):
    print(f"{addr} -> connection start")

    with sock:
        yield from read_ready(sock)
        request = sock.recv(1024)
        print(f"{addr} received -> {request}")

        if SIMULATE_SLOW_IO:
            yield from sleep(random.randint(0, 2))

        request = b"pong" if request == b"ping" else request
        response = request.upper()

        print(f"{addr} response <- {response}")
        sock.send(response)

    print(f"{addr} <- connection end")


def start_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv_sock:
        srv_sock.bind((host, port))
        srv_sock.setblocking(False)
        srv_sock.listen(1)

        print(f"Starting server at {host}:{port}")

        while True:
            yield from read_ready(srv_sock)
            client_sock, addr = srv_sock.accept()
            client_sock.setblocking(False)
            create_task(handle_request(client_sock, addr))


if __name__ == "__main__":
    loop(start_server(HOST, PORT))
