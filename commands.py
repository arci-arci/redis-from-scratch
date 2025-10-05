from typing import TypedDict

class CommandInformationType(TypedDict):
    name: str
    args: int


commands: dict[str, CommandInformationType] = {
    "PING": {
        "name": "PING",
        "args": 0
    },
    "EXIT": {
        "name": "EXIT",
        "args": 0
    },
    "GET": {
        "name": "GET",
        "args": 1
    },
    "SET": {
        "name": "SET",
        "args": 2
    },
    "EXISTS": {
        "name":"EXISTS",
        "args": 1,
    },
    "HELP": {
        "name": "HELP",
        "args": 0
    }
}


class ValidateCommand:
    def is_a_command(self, command: str) -> bool:
        value: CommandInformationType | None = commands.get(command)
        return value != None



def show_help() -> None:
    print("Usage: COMMAND [<KEY>] [<VALUE>]")

    print("\nAvaiable commands:\n")
    print("PING                 Check if the server is on")
    print("EXIT                 Disconnect from the server")
    print("GET <KEY>            Get a key from the store")
    print("SET <KEY> <VALUE>    Set a key-value pair in the store")
    print("EXISTS <KEY>         Check if a key is stored in the store, returning his value if exits. Other (nil)")
    print("HELP                 Show a description of all commands")