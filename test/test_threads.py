import os
import sys
sys.path.append(os.path.abspath("./src"))

from utility.commons import BUFFER_SIZE, HOST, PORT
from socket import socket, AF_INET, SOCK_STREAM
import threading
import random

def gen_key_value():
    keys = ["bike", "car", "truck"]
    values = [250, 500, 750]

    
    random.shuffle(keys)
    random.shuffle(values)

    rv = random.choice(values)
    rk = random.choice(keys)

    return (rk, rv)

def connect() -> None:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        commands = ["SET", "GET"]

        for _ in range(2):    
            command = random.choice(commands)
            if command == "SET":
                for _ in range(5):
                    key, value = gen_key_value()
                    final_command = f"{command} {key} {value}"

                    raw_data = bytes(final_command, "utf-8")
                    s.sendall(raw_data)

                    raw_data: bytes = s.recv(BUFFER_SIZE)
                    data: str = raw_data.decode("utf-8")
                    print(data)
            if command == "GET":
                 for _ in range(5):
                    key, value = gen_key_value()
                    final_command = f"{command} {key}"

                    raw_data = bytes(final_command, "utf-8")
                    s.sendall(raw_data)

                    raw_data: bytes = s.recv(BUFFER_SIZE)
                    data: str = raw_data.decode("utf-8")
                    print(data)


if __name__ == "__main__":
    thread_amount: int = 2
    threads: list[threading.Thread] = []

    for _ in range(thread_amount):
        t = threading.Thread(target=connect)
        threads.append(t)

    for t in threads:
        t.start()
