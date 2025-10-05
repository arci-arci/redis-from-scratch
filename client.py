import socket
from commons import HOST, PORT, BUFFER_SIZE


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            user_input = bytes(input("badis> "), "utf-8")
        
            s.sendall(user_input)
            raw_data: bytes = s.recv(BUFFER_SIZE)
            data: str = raw_data.decode("utf-8")

            if data == "EXIT":
                break

