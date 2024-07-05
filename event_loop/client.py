import socket

from event_loop import loop, read_ready, create_task, sleep


def ping(host: str, port: int, data: bytes = b"ping"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setblocking(False)

        print(f"Request -> {host}:{port}")
        sock.connect_ex((host, port))
        sock.send(data)

        yield from read_ready(sock)
        response = sock.recv(64)
        print("Response <-", response)


if __name__ == "__main__":
    from server import HOST, PORT

    def main(timeout: int = 3):
        for i in range(5):
            create_task(ping(HOST, PORT, str(i).encode()))

        yield from sleep(timeout)
        exit()

    loop(main())
