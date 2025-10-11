import os
from dotenv import load_dotenv

load_dotenv()

_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORT = "6969"

HOST: str = os.environ.get("RE_HOST") or  _DEFAULT_HOST
PORT: int = int(os.environ.get("RE_PORT_NUMBER") or _DEFAULT_PORT)
BUFFER_SIZE: int = 1024

