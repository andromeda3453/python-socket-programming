import socket
import threading

# define length of header message that server will receive when connection is established
HEADER = 64
# random number for port, one that is not used by other programs
PORT = 5050
# using local machine as a server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# define decoding format
FORMAT = 'utf-8'
# message to be sent to disconnect from server
DISCONNECT_MESSAGE = '!DISCONNECT'

# creating a new socket, AF_INET means using ipv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding that socket to the given ip address and port
server.bind(ADDR)


def handle_client(conn, addr):
    """
    function that will handle connections to clients 
    """
    print(f"[NEW CONNECTION] {addr} has connected")

    connected = True
    while connected:
        # recv is a blocking function
        # first message will tell us the length of the actual message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        # second message will be the actual message
        msg = conn.recv(msg_length).decode(FORMAT)
        print(f"[{addr}] {msg}")

        if msg == DISCONNECT_MESSAGE:
            connected = False

    conn.close()


def start():
    """
    will start the server and listen for new connections.
    once new connection comes in it will pass it to the handle client function in a new thread
    that will handle the connection

    """

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:

        # server.recieve is a blocking function
        # when sever accepts a connection, it returns the address of the client plus a conn object which we can use to communicate with the client
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # print number of current connections. minusing 1 because main thread is included in count
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


print("[STARTING] Server is starting....")
start()
