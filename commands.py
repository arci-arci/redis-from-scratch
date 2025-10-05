commands: dict[str, str] = {
    "PING": "PING",
    "EXIT": "EXIT",
    "GET": "GET",
    "SET": "SET",
    "EXISTS": "EXISTS",
    "HELP": "HELP"
}


class ValidateCommand:
    def is_valid(self, command: str) -> bool:
        value: str | None = commands.get(command)
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