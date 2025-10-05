import socket
from commons import HOST, PORT, BUFFER_SIZE

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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

                if data == "PING":
                    conn.sendall(bytes("PONG", "utf-8"))
                elif data == "EXIT":
                    conn.sendall(bytes("EXIT", "utf-8"))
                    break
                else:
                    conn.sendall(bytes("SHIT", "utf-8"))

            conn.close()