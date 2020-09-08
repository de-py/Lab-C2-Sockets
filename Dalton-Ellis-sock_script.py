import http.server
import threading
import ssl
import socket

# Modifying do_GET function from BaseHTTPRequestHandler to reply with html.
class http_server(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'<html>Dalton Ellis<br></html>')

# Serving HTTP with HTTP Server module
def http_requests(http_port):
    serve = http.server.HTTPServer(('localhost',http_port), http_server)
    serve.serve_forever()

# Wrapping HTTP server module socket in SSL to serve HTTPS
def https_requests(https_port):
    serve = http.server.HTTPServer(('localhost',https_port), http_server)
    serve.socket = ssl.wrap_socket(serve.socket, keyfile="840.pem", certfile="840cert.pem", server_side=True)
    serve.serve_forever()


# Handles the responses to each individual leet connection
def handle_leet_request(conn, addr, context):
    try:
        ssock = context.wrap_socket(conn, server_side=True)
        with ssock:
            print("Connection from", addr)

            while True:
                data = ssock.recv(1024)

                # If string is hacks from client, print "you are hacked"
                if "hacks" in str(data):
                    # pass
                    data = b'You are hacked by Dalton Ellis - Server\n'
                    ssock.sendall(data)
                
                # If exit sent from client, closes that connection
                elif "exit" in str(data):
                    ssock.send(b"Goodbye - Server\n")
                    break
                # If any other type of message is sent
                else:
                    data = b'Nothing to see here. - Server\n'
                    ssock.sendall(data)
                
                # End if not actually data
                if not data: break

    # Exception allows for the closure of non-SSL connections and will continue to listen without blocking listener.
    except Exception as e:
        if "ssl" in str(e):
            print("There's a good chance that's not SSL.")
        else:
            print("Client exited. Goodbye")

    print("Closing", addr)       
    conn.close()



# Listening for new leet connection and spawning a new thread when it receives one.
def thread_me(s, context):
    while True:
        conn, addr = s.accept()
        
        try:            
            t = threading.Thread(target=handle_leet_request, args=(conn,addr, context))
            t.start()

        except:
            print('There\'s a good chance that\'s not SSL')


# Handles leet socket set up and sends to threading function
def leet_sock(port):
    HOST = 'localhost'
    PORT = port
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('840cert.pem', '840.pem')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(4)

    # Sends socket listener to threading function. Previously this supported 3 sockets (http, https, l337) so it became it's own function.
    thread_me(s, context)
        


def main():
    http_port = 8080
    https_port = 4443
    l337_port = 1337


    # Start http server in it's own thread
    http = threading.Thread(target=http_requests, args=(http_port,))
    http.start()

    # Start https server in it's own thread
    https = threading.Thread(target=https_requests, args=(https_port,))
    https.start()

    # Start 1337 socket in it's own thread.
    leet = threading.Thread(target=leet_sock, args=(l337_port,))
    leet.start()
    
   

if __name__ == "__main__":
    main()


