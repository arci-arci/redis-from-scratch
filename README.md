# Redis from scratch in Python
A basic implementation on how redis work made in Python.

## Description
The aim of this project is to have a better understanding on the Python programming language and, how to handle multiple 
threads in a client-server architecture, how to handle thread-safety using locks primitives, logging using both the console and save them 
inside a text file using custom templates, handling time-to-live with automatic cleanup and using a Pyright as a static type checker
to ensure more stability.

The client is an interactive CLI where you use the send commands and the server handle requests, from multiple clients, and entry's ttl.

## Implemented Commands
- `HELP`: Show a full list of avaiable commands with their description;
- `EXIT`: Close a connection to the server;
- `PING`: Check if the server is up and running;
- `GET`: Retrive a key;
- `EXISTS`: Check if a key exists;
- `SET`: Add a key or override his current value if is exists;
- `DEL`: Remove a key, if exists;
- `EXPIRE`: Set an expiration time, in seconds, on a key.

## How to run

1. [Install](https://docs.astral.sh/uv/getting-started/installation/) the uv package and project manager;
2. Create a new virtual environment using the `uv venv` command;
3. Run `sh run-server.sh` command to run the server. During this step, uv should install automatically all the project's dependencies;
4. Run `sh client-server.sh` command to run the client.

## Next Steps
- Adding Pub/Sub commands
- Limit the number of concurrent connections
- Adding commands for manipulating Lists, Sets and Hash Tables

