import socket
import select
import errno
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
name = input("what is your name: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
username = name.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
while True:
    msg = input(f'{name} > ')
    if msg:
        msg = msg.encode('utf-8')
        msg_x = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(msg_x + msg)
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print('Connection terminated by the server')
                sys.exit()
            name_len = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(name_len).decode('utf-8')
            msg_x = client_socket.recv(HEADER_LENGTH)
            msg_len = int(msg_x.decode('utf-8').strip())
            msg = client_socket.recv(msg_len).decode('utf-8')
            print(f'{username} > {msg}')
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            sys.exit()
        continue
    except Exception as e:
        sys.exit()