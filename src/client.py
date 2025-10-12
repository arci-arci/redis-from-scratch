from socket import socket, AF_INET, SOCK_STREAM
from utility.commons import HOST, PORT, BUFFER_SIZE
from utility.commands import check_user_input, show_help, CommandEnum


if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            user_input = input("repy> ").strip()
            if not check_user_input(user_input):
                print(f"Command '{user_input}' is not a valid command")
                continue
            
            command_struct: list[str] = user_input.split(" ")
            command_type: str = command_struct[0].upper()

            if command_type == CommandEnum.HELP:
                show_help()
                continue

            raw_data = bytes(user_input, "utf-8")
            s.sendall(raw_data)

            raw_data: bytes = s.recv(BUFFER_SIZE)
            data: str = raw_data.decode("utf-8")
            print(data)

            if data == "EXIT":
                break

