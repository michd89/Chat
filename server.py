import socket
import threading

host = '127.0.0.1'  # TODO: Change to alles oder so?
port = 50000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f'Server horcht auf {host}:{port} ...')

clients = []
nicknames = []


# Sends messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Sub thread: Handles messages from clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            # TODO: Handle '/gusten'
            broadcast(message)
        except:
            # Remove and close client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} hat den Chat verlassen!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Main thread: Receiving / Listening function
def receive():
    while True:
        # Accept connection
        client, address = server.accept()
        print("Verbunden mit {}".format(str(address)))

        # Request and store nickname
        client.send('NICK'.encode('ascii'))  # TODO: Können Nutzer damit Unsinn treiben, indem sie nur NICK schreiben?
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname
        print("Name ist {}".format(nickname))
        broadcast("{} ist dem Chat beigetreten!".format(nickname).encode('ascii'))
        client.send('Verbindung hergestellt!'.encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))  # TODO: Geht das nicht auch ohne Komma?
        thread.start()


if __name__ == '__main__':
    receive()
