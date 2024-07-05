import socket

from event_loop import loop
from server import HOST, PORT


def ping(host: str, port: int, data: bytes = b"ping"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setblocking(False)
        print(f"Request -> {host}:{port}")
        sock.connect_ex((host, port))
        sock.send(data)
        yield sock
        print("Response <-", sock.recv(64))


if __name__ == "__main__":
    def main():
        yield from ping(HOST, PORT)
        exit()

    # loop(ping(HOST, PORT))
    loop(main())
