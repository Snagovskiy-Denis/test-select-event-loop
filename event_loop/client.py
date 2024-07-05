import socket

from event_loop import loop, read_ready, write_ready, create_task, sleep


def ping(host: str, port: int, data: bytes = b"ping"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setblocking(False)

        print(f"{host}:{port} -> {data}")
        sock.connect_ex((host, port))

        yield from write_ready(sock)
        sock.send(data)

        yield from read_ready(sock)
        response = sock.recv(64)
        print(f"{host}:{port} <- {response}")


if __name__ == "__main__":
    from server import HOST, PORT

    def main(timeout: int = 4):
        for i in range(10):
            create_task(ping(HOST, PORT, f"id={i}".encode()))

        yield from sleep(timeout)
        exit()

    loop(main())
