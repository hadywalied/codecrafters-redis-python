# Uncomment this to pass the first stage
import socket
import threading
import re

class Regexes :
    PING_REGEX = re.compile(r'ping\b', re.IGNORECASE)
    ECHO_REGEX = re.compile(r'echo\b(.*)', re.IGNORECASE)
    

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
