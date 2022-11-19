# -*- coding: utf-8 -*-
"""part2_server.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zw7McfOqdQ3IJy9OyX5GDzN_8dZTO6-2
"""

import socket
import select

IP = "127.0.0.1"
PORT = 1235
HEADER_LENGTH = 10
disconnect_msg = "exit"

sskt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sskt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sskt.bind((IP, PORT))
sskt.listen()
sockets_list = [sskt]
clients = {}
print(f'Listening for connections on {IP}:{PORT}...')

def receive_message(client_socket):
    msg_x = client_socket.recv(HEADER_LENGTH)
    if not len(msg_x):
        return False
    msg_len = int(msg_x.decode('utf-8').strip())
    return {'header': msg_x, 'data': client_socket.recv(msg_len)}

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == sskt:
            client_socket, client_address = sskt.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print('New connection Accepted from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Connection Closed from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            elif message == disconnect_msg:
                break
            user = clients[notified_socket]
            print(f'Message Received from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])