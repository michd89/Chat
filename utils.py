ENCODING = 'ascii'
RECV_SIZE = 1024


def send_msg(sock, msg):
    sock.send(msg.encode(ENCODING))


def recv_msg(sock):
    return sock.recv(RECV_SIZE).decode(ENCODING)
