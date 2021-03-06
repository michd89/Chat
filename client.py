import socket
import threading

from utils import send_msg, recv_msg

port = 50000

host = input('Hostname oder IP (leer = localhost): ')
if not host:
    host = 'localhost'
nickname = input('Name: ')

# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


# Sends messages to server
def write():
    while True:
        message = '<{}> {}'.format(nickname, input(''))
        send_msg(client, message)


# Listens to server and sending nickname
def receive():
    while True:
        try:
            # Receive message from server
            # If 'NICK' send nickname
            message = recv_msg(client)
            if message == 'NICK':
                send_msg(client, nickname)
            else:
                print(message)
        except:
            # Close connection when error
            print("Fehler!")
            client.close()
            break


if __name__ == '__main__':
    # Starting threads for listening and writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
