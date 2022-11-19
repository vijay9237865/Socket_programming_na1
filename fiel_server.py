# importing reqiuired libraries
import socket
IP = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
def main():
    print("starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("Server is listening...")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        filename = conn.recv(SIZE).decode(FORMAT)
        file = open(filename, "w")
        conn.send("Filename received.".encode(FORMAT))
        data = conn.recv(SIZE).decode(FORMAT)
        file.write(data)
        conn.send("File data received".encode(FORMAT))
        file.close()
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")
if __name__ == "__main__":
    main()
