# Uncomment this to pass the first stage
import socket
import threading
import re

class Regexes :
    PING_REGEX = re.compile(r'ping\b', re.IGNORECASE)
    ECHO_REGEX = re.compile(r'echo\b(.*)', re.IGNORECASE)
    GET_REGEX = re.compile(r'get\b(.*)', re.IGNORECASE)
    SET_REGEX = re.compile(r'set\b(.*)', re.IGNORECASE)


STORAGE = {}


def handle(connection):
    with connection:
        while True:
            data = connection.recv(1024).decode()
            if re.search(Regexes.PING_REGEX, data):
                connection.sendall(b"+PONG\r\n")
            elif re.search(Regexes.ECHO_REGEX, data):
                resp = data.split("\r\n")[-2]
                resp = f"${len(resp)}\r\n{resp}\r\n"
                resp = resp.encode()
                connection.sendall(resp)
            elif re.search(Regexes.SET_REGEX, data):
                key, value = data.split("\r\n")[-4], data.split("\r\n")[-2]
                STORAGE[key] = value
                resp = b'+OK\r\n'
                # resp = resp.encode()
                connection.sendall(resp)
            elif re.search(Regexes.GET_REGEX, data):
                key = data.split("\r\n")[-2]
                resp = f"${len(STORAGE[key])}\r\n{STORAGE[key]}\r\n" if key in STORAGE.keys() else '$-1\r\n'
                # resp = f"${len(resp)}\r\n{resp}\r\n"
                resp = resp.encode()
                connection.sendall(resp)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    while True:
        connection, _ =server_socket.accept() # wait for client
        _thread = threading.Thread(target= handle, args=[connection])
        _thread.start()


if __name__ == "__main__":
    main()
