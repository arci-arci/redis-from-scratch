from socket import socket, AF_INET, SOCK_STREAM
from commons import HOST, PORT, BUFFER_SIZE
from commands import ValidateCommand, show_help

if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        validator = ValidateCommand()

        while True:
            user_input = input("repy> ").strip()
            command_type: str = user_input.split(" ")[0]

            if not validator.is_a_command(command_type):  
                print(f"Command {user_input} is not a valid command")
                continue

            if command_type == "HELP":
                show_help()
                continue
            
            raw_data = bytes(user_input, "utf-8")
            s.sendall(raw_data)

            raw_data: bytes = s.recv(BUFFER_SIZE)
            data: str = raw_data.decode("utf-8")
            print(data)


            if data == "EXIT":
                break

