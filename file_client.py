#importing required libraries
import threading
import socket

#assigning IP address
IP = socket.gethostbyname(socket.gethostname())

#assigning the port
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"

#size
SIZE = 1024
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    file = open("hello.txt", "r")
    data = file.read()
    client.send("hello.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    file.close()
    client.close()
if __name__ == "__main__":
    main()
