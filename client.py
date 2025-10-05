import socket
from commons import HOST, PORT, BUFFER_SIZE
from commands import ValidateCommand, show_help

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        validator = ValidateCommand()

        while True:
            user_input = input("repy> ").strip()

            if not validator.is_a_command(user_input): 
                print(f"Command {user_input} is not a valid command")
                continue
            
            if user_input == "HELP":
                show_help()
            

            raw_data = bytes(user_input, "utf-8")
            s.sendall(raw_data)

            raw_data: bytes = s.recv(BUFFER_SIZE)
            data: str = raw_data.decode("utf-8")
            print(f"data: {data}")


            if data == "EXIT":
                break

