import socket
import threading

def response_200():
    response = (
    b"HTTP/1.1 200 OK\n"
    b"Content-Length: 18\n"
    b"Connection: Keep-Alive\n"
    b"Content-Type: text/html\n\n"
    b"<html>\n"
    b"hi\n"
    b"</html>\n"
    )


    return response

def response_503():
    response = (
    b"HTTP/1.1 503 Internal Server Error\n"
    b"Content-Length: 65\n"
    b"Content-Type: text/html\n\n"
    b"<html>\n"
    b"An error has Occured. We only accept GET requests\n"
    b"</html>\n"
    )


    return response


# Handles the responses to each individual connection
def handle_request(conn, addr):
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            # If Get request send a 200
            if "GET" in str(data):
                # pass
                data = response_200()
                conn.sendall(data)
            
            # If exit sent from client, closes that connection
            elif "exit" in str(data):
                conn.send(b"Goodbye\n")
                break
            # If any other type of request is sent
            else:
                # End if not actually data
                if not data: break

                # If data is sent but not a GET request or EXIT call, send a 503 error.
                data = response_503()
                conn.sendall(data)


    print("Closing", addr)       
    conn.close()

# Listening for new connections and spawning a new thread when it receives one.
def thread_me(s):
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_request, args=(conn,addr))
        t.start()


# Handles socket set up and sends to threading function
def socks(port):
    HOST = ''
    PORT = port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(4)

    # Sends socket listener to threading function
    thread_me(s)




def main():
    http_port = 8080
    https_port = 443


    # Start http socket in it's own thread
    http = threading.Thread(target=socks, args=(http_port,))
    http.start()

    # Start https socket in it's own thread
    https = threading.Thread(target=socks, args=(https_port,))
    https.start()


if __name__ == "__main__":
    main()