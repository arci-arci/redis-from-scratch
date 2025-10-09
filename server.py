from socket import socket, AF_INET, SOCK_STREAM
from commands import CommandEnum, CommandLenEnum
from commons import HOST, PORT, BUFFER_SIZE
from logconfig import create_logger, log_action

storage: dict[str, str] = {}
logger = create_logger()

class ActionHandler:
    def __init__(self, conn: socket):
        self.conn = conn

    @log_action(CommandEnum.PING, logger)
    def run_ping_command(self) -> None:
        self.conn.sendall(bytes("PONG", "utf-8"))

    @log_action(CommandEnum.EXIT, logger)
    def run_exit_command(self) -> None:
        self.conn.sendall(bytes("EXIT", "utf-8"))

    @log_action(CommandEnum.SET, logger)
    def run_set_command(self, key: str, value: str) -> None:    
        storage[key] = value
        self.conn.sendall(bytes("OK", "utf-8"))

    @log_action(CommandEnum.GET, logger)
    def run_get_command(self, key: str) -> None:
        if key in storage:
            value: str = storage[key]
            logger.info("Key '%s' found", key)
            self.conn.sendall(bytes(value, "utf-8"))
        else:
            logger.info("Key '%s' not found", key)
            self.conn.sendall(bytes("(null)", "utf-8"))

    @log_action(CommandEnum.EXISTS, logger)
    def run_exists_command(self, key: str) -> None:
        if key in storage:
            logger.info("Key '%s' found", key)
            self.conn.sendall(bytes("(true)", "utf-8"))
        else:
            logger.info("Key '%s' not found", key)
            self.conn.sendall(bytes("(false)", "utf-8"))

if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"Server is running at: http://{HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            action_handler = ActionHandler(conn)
            
            while True:
                raw_data: bytes = conn.recv(BUFFER_SIZE)
                if not raw_data:
                    break
                
                data = raw_data.decode("utf-8")
                logger.info("Data received: '%s'", data)

                command_struct: list[str] = data.split(" ")
                command_type: str = command_struct[0]

                match command_type:
                    case CommandEnum.PING:
                        action_handler.run_ping_command()
                    case CommandEnum.SET:
                        command_data = data.split(" ", CommandLenEnum.TWO)
                        action_handler.run_set_command(command_data[1], command_data[2])
                    case CommandEnum.GET:
                        command_data = data.split(" ", CommandLenEnum.ONE)
                        action_handler.run_get_command(command_data[1])
                    case CommandEnum.EXISTS:
                        command_data = data.split(" ", CommandLenEnum.ONE)
                        action_handler.run_exists_command(command_data[1])
                    case CommandEnum.EXIT:
                        action_handler.run_exit_command()
                        break
            
            conn.close()