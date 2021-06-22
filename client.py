import socket
import threading

host = '127.0.0.1'  # TODO: Change to input
port = 50000

# Choosing nickname
nickname = input("Name: ")

# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


# Sends messages to server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


# Listens to server and sending nickname
def receive():
    while True:
        try:
            # Receive message from server
            # If 'NICK' send nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
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
