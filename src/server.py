from socket import socket, AF_INET, SOCK_STREAM
from threading import Event, Thread, RLock, get_ident
from utility.commands import CommandEnum
from utility.commons import HOST, PORT, BUFFER_SIZE
from utility.logconfig import LogSinleton, log_action
from typing import TypedDict
import time
import datetime

class Element(TypedDict):
    value: str
    ttl: datetime.time

storage: dict[str, Element] = {}
lock = RLock()
logger = LogSinleton.create_logger()
exit_event = Event()

DEFAULT_TTL: int = 60 # in seconds
TTL_INTERVAL: float = 60.0 # check every minute

class ActionHandler:
    def __init__(self, conn: socket):
        self.conn = conn

    @log_action(CommandEnum.PING)
    def run_ping_command(self) -> None:
        self.conn.sendall(bytes("PONG", "utf-8"))

    @log_action(CommandEnum.EXIT)
    def run_exit_command(self) -> None:
        self.conn.sendall(bytes("EXIT", "utf-8"))

    @log_action(CommandEnum.SET)
    def run_set_command(self, key: str, value: str) -> None:
        with lock:
            ttl = datetime.datetime.now() + datetime.timedelta(seconds=DEFAULT_TTL)
            is_present: bool = key in storage
            storage[key] = {"ttl": ttl.time(), "value": value}

            if not is_present:
                logger.info(f"{key} -> {storage[key]} added by {get_ident()}")
            else:
                logger.info(f"{key} -> {storage[key]} changed by {get_ident()}")

            self.conn.sendall(bytes("OK", "utf-8"))
            
    @log_action(CommandEnum.GET)
    def run_get_command(self, key: str) -> None:
        if key not in storage:
            logger.info(f"Key '%s' not found by thread %d", key, get_ident())
            self.conn.sendall(bytes("(null)", "utf-8"))
            return

        if is_exprired(key):
            logger.info(f"Key '%s' not found by thread %d", key, get_ident())
            self.conn.sendall(bytes("(null)", "utf-8"))
            return

        e: Element = storage[key]
        logger.info("Key '%s' found by thread %d with value %s", key, get_ident(), e["value"])
        self.conn.sendall(bytes(e["value"], "utf-8"))

    @log_action(CommandEnum.EXISTS)
    def run_exists_command(self, key: str) -> None:
        if key not in storage:
            logger.info(f"Key '%s' not found by thread %d", key, get_ident())
            self.conn.sendall(bytes("(false)", "utf-8"))
            return

        if is_exprired(key):
            logger.info(f"Key '%s' not found by thread %d", key, get_ident())
            self.conn.sendall(bytes("(false)", "utf-8"))
            return

        logger.info("Key '%s' found by thread %d", key, get_ident())
        self.conn.sendall(bytes("(true)", "utf-8"))

    @log_action(CommandEnum.DEL)
    def run_del_command(self, key: str) -> None:
        with lock:
            if key not in storage:
                logger.info(f"Key '%s' not found by thread %d", key, get_ident())
                self.conn.sendall(bytes("(false)", "utf-8"))
                return

            if is_exprired(key):
                logger.info("Key '%s' removed by thread %d", key, get_ident())
                self.conn.sendall(bytes("(true)", "utf-8"))
                return

            del storage[key]
            logger.info("Key '%s' removed by thread %d", key, get_ident())
            self.conn.sendall(bytes("(true)", "utf-8"))

    @log_action(CommandEnum.EXPIRE)
    def run_expire_command(self, key: str, exp: int) -> None:
        with lock:
            if key not in storage:
                logger.info(f"Key '%s' not found by thread %d", key, get_ident())
                self.conn.sendall(bytes("ERR", "utf-8"))
                return

            if is_exprired(key):
                logger.info("Key '%s' removed by thread %d", key, get_ident())
                self.conn.sendall(bytes("ERR", "utf-8"))
                return

            new_ttl = datetime.datetime.now() + datetime.timedelta(seconds=exp)
            logger.info("New ttl %s for key '%s'", new_ttl.time(), key)
            storage[key]["ttl"] = new_ttl.time()
            logger.info("Expiration time updated for key '%s' by thread %d", key, get_ident())
            self.conn.sendall(bytes("OK", "utf-8"))


def is_exprired(key: str) -> bool:
    e: Element = storage[key]
    return datetime.datetime.now().time() > e["ttl"]

def clean() -> None:
    start_time = time.monotonic()

    while not exit_event.is_set():
        exit_event.wait(TTL_INTERVAL - ((time.monotonic() - start_time) % TTL_INTERVAL))
        prev_size: int = len(storage)

        with lock:
            items = list(storage.keys())
            for k in items:
                if is_exprired(k):
                    e: Element = storage[k]
                    del storage[k]
                    logger.info(f"Entry {k}: {e} removed from storage")

        if prev_size > 0:
            new_size: int = len(storage)
            difference = ((prev_size - new_size) / prev_size) * 100
            logger.info(f"Cleaning done. Removed {prev_size - new_size} element(s). Size reduced by a {difference}%")
            
    logger.info("Stopping clean thread...")


def start_connection(conn: socket, addr: tuple[str, int]) -> None:
    logger.info(f"Client connected from {addr[0]}:{addr[1]}")
    action_handler = ActionHandler(conn)
    
    while True:
        raw_data: bytes = conn.recv(BUFFER_SIZE)
        if not raw_data:
            break
        
        data = raw_data.decode("utf-8")
        logger.info("Data received: '%s'", data)

        command_struct: list[str] = data.split(" ")
        command_type: str = command_struct[0].upper()

        match command_type:
            case CommandEnum.PING:
                action_handler.run_ping_command()
            case CommandEnum.SET:
                command_data = data.split(" ", 2)
                action_handler.run_set_command(
                    command_data[1], 
                    command_data[2]
                )
            case CommandEnum.GET:
                command_data = data.split(" ", 1)
                action_handler.run_get_command(command_data[1])
            case CommandEnum.DEL:
                command_data = data.split(" ", 1)
                action_handler.run_del_command(command_data[1])
            case CommandEnum.EXISTS:
                command_data = data.split(" ", 1)
                action_handler.run_exists_command(command_data[1])
            case CommandEnum.EXPIRE:
                command_data = data.split(" ", 2)
                action_handler.run_expire_command(
                    command_data[1],
                    int(command_data[2]),
                )
            case CommandEnum.EXIT:
                action_handler.run_exit_command()
                break

    conn.close()


if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"Server is running at: http://{HOST}:{PORT}")

        ttl_thread: Thread = Thread(target=clean)
        ttl_thread.start()
        
        try:
            while True:
                conn, addr = s.accept()
                t: Thread = Thread(target=start_connection, args=(conn, addr))
                t.start()
        except KeyboardInterrupt:
            exit_event.set()
            logger.info("Stopping server...")