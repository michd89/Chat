import re
import socket
import threading

from utils import recv_msg, send_msg

host = '0.0.0.0'
port = 50000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f'Server horcht auf {host}:{port} ...')

clients = []
nicknames = []


def get_users_message():
    return 'Anwesende Gusten: ' + ', '.join(nicknames)


# Sends messages to all connected clients
def broadcast(message, exceptions=[]):
    for client in clients:
        if client not in exceptions:
            send_msg(client, message)


# Sub thread: Handles messages from clients
def handle(client):
    while True:
        try:
            message = recv_msg(client)
            if re.search(r'^<.+> /gusten$', message):
                send_msg(client, get_users_message())
            else:
                broadcast(message)
        except:
            # Remove and close client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            msg = '{} hat den Chat verlassen!'.format(nickname)
            print(msg)
            broadcast(msg)
            nicknames.remove(nickname)
            break


# Main thread: Receiving / Listening function
def receive():
    while True:
        # Accept connection
        client, address = server.accept()
        print("Verbunden mit {}".format(str(address)))

        # Request and store nickname
        send_msg(client, 'NICK')
        nickname = recv_msg(client)
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname
        print("Name ist {}".format(nickname))
        send_msg(client, 'Verbindung hergestellt!')
        send_msg(client, get_users_message())
        broadcast("{} ist dem Chat beigetreten!".format(nickname), [client])

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=([client]))
        thread.start()


if __name__ == '__main__':
    receive()
