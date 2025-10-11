from enum import StrEnum, IntEnum

class CommandEnum(StrEnum):
    PING = "PING"
    EXIT = "EXIT"
    HELP = "HELP"
    GET = "GET"
    EXISTS = "EXISTS"
    SET = "SET"
    DEL = "DEL"

class CommandLenEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3


def check_user_input(user_input: str) -> bool:
    command_struct: list[str] = user_input.split(" ")
    command_type: str = command_struct[0]

    if not __is_a_command(command_type):  
        return False
        
    has_zero_args: bool = __is_a_valid_zero_args_command(user_input)
    has_one_args: bool = __is_a_valid_one_args_command(user_input)
    has_two_args: bool = __is_a_valid_two_args_command(user_input)
      
    return has_zero_args or has_one_args or has_two_args

def show_help() -> None:
    print("Usage: COMMAND [<KEY>] [<VALUE>]")

    print("\nAvaiable commands:\n")
    print("PING                 Check if the server is on")
    print("EXIT                 Disconnect from the server")
    print("GET <KEY>            Get a key from the store")
    print("DEL <KEY>            Remove a key from the store")
    print("SET <KEY> <VALUE>    Set a key-value pair in the store")
    print("EXISTS <KEY>         Check if a key is stored in the store")
    print("HELP                 Show a description of all commands")

def __is_a_command(command: str) -> bool:
    try:
        CommandEnum[command]
    except KeyError:
        return False
    return True

def __is_a_valid_two_args_command(command: str) -> bool:
    command_struct: list[str] = command.split(" ")

    if len(command_struct) != 3:
        return False
    
    command_type: str = command_struct[0]
    is_set_command: bool = command_type == CommandEnum.SET

    return is_set_command

def __is_a_valid_one_args_command(command: str) -> bool:
    command_struct: list[str] = command.split(" ")
    
    if len(command_struct) != 2:
        return False
    
    command_type: str = command_struct[0]
    is_get_command: bool = command_type == CommandEnum.GET  
    is_del_command: bool = command_type == CommandEnum.DEL  
    is_exists_command: bool = command_type == CommandEnum.EXISTS

    return is_get_command or is_exists_command or is_del_command

def __is_a_valid_zero_args_command(command: str) -> bool:
    command_struct: list[str] = command.split(" ")
    command_type: str = command_struct[0]

    if len(command_struct) != 1:
        return False
    
    is_help_command: bool = command_type == CommandEnum.HELP 
    is_exit_command: bool = command_type == CommandEnum.EXIT 
    is_ping_command: bool = command_type == CommandEnum.PING
    
    return is_help_command or is_exit_command or is_ping_command

