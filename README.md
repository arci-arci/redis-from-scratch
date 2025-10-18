# Redis from scratch in Python
A basic implementation of how Redis works made in Python.

## Description
The aim of this project is to have a better understanding of the Python programming language and how to handle multiple threads in a client-server architecture, how to handle thread-safety using lock primitives, logging to both the console and save logs inside a text file using custom templates, handling time-to-live with automatic cleanup, and using Pyright as a static type checker to ensure greater stability.

The client is an interactive CLI where you send commands and the server handles requests from multiple clients and entry TTLs.

## Implemented Commands
- `HELP`: Show a full list of available commands with their descriptions;
- `EXIT`: Close a connection to the server;
- `PING`: Check if the server is up and running;
- `GET`: Retrieve a key;
- `EXISTS`: Check if a key exists;
- `SET`: Add a key or override its current value if it exists;
- `DEL`: Remove a key, if it exists;
- `EXPIRE`: Set an expiration time, in seconds, on a key.

## How to run

1. [Install](https://docs.astral.sh/uv/getting-started/installation/) the uv package manager;
2. Create a new virtual environment using the `uv venv` command;
3. Optional: Create a `.env` file in the root of the folder and set up the following values:
    - `RE_HOST`: IP address of the server, by default it is localhost;
    - `RE_PORT_NUMBER`: Port number of the server, by default it is 6969;
4. Run `sh run-server.sh` to start the server. During this step, uv should automatically install all the project's dependencies;
5. Run `sh run-client.sh` to start the client.

## Next Steps
- Add Pub/Sub commands
- Limit the number of concurrent connections
- Add commands for manipulating Lists, Sets, and Hash Tables
