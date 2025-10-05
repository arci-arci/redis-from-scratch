from socket import socket, AF_INET, SOCK_STREAM
from commons import HOST, PORT, BUFFER_SIZE

storage: dict[str, str] = {}


def __run_ping_command(conn: socket) -> None:
    conn.sendall(bytes("PONG", "utf-8"))

def __run_exit_command(conn: socket) -> None:
    conn.sendall(bytes("EXIT", "utf-8"))

def __run_set_command(conn: socket, key: str, value: str) -> None:
    storage[key] = value
    conn.sendall(bytes("OK", "utf-8"))

def __run_get_command(conn: socket, key: str) -> None:
    if key in storage:
        value: str = storage[key]
        conn.sendall(bytes(value, "utf-8"))
    else:
        conn.sendall(bytes("(null)", "utf-8"))

def __run_exists_command(conn, key: str) -> None:
    if key in storage:
        conn.sendall(bytes("(true)", "utf-8"))
    else:
        conn.sendall(bytes("(false)", "utf-8"))

if __name__ == "__main__":
  with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is running at: http://{HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        
        while True:
            raw_data: bytes = conn.recv(BUFFER_SIZE)
            if not raw_data:
                break
            
            data = raw_data.decode("utf-8")
            command_struct: list[str] = data.split(" ")
            command_type: str = command_struct[0]

            match command_type:
                case "PING":
                    __run_ping_command(conn)
                case "SET":
                    command_data = data.split(" ", 2)
                    __run_set_command(conn, command_data[1], command_data[2])
                case "GET":
                    command_data = data.split(" ", 1)
                    __run_get_command(conn, command_data[1])
                case "EXISTS":
                    command_data = data.split(" ", 1)
                    __run_exists_command(conn, command_data[1])
                case "EXIT":
                    __run_exit_command(conn)
                    break
          
        conn.close()