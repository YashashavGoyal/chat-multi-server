## Importing Modules
from concurrent.futures import ThreadPoolExecutor
import socket
## ........


class SocketServer:

    clients = []
    clientsAddr = {}

    ## Constructor
    def __init__(self, host:tuple):
        self.host_ip = host[0]
        self.host_port = host[1]
    ## ......

    ## Start Server method
    def _startServer(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.soc.bind((self.host_ip, self.host_port))
            self.soc.listen(5)
        except socket.error as err:
            print("Socket failed with err : %s" %(err))
        else:
            print(f"Server is listening on {self.host_ip}:{self.host_port}")
            # self.soc.settimeout(20)  # set waiting time 
    ## .........
    
    ## Client Connecting Method
    def _connectClient(self):
        try:
            conn, addr = self.soc.accept()

            if conn:
                print(f"Connected to {addr}")
                conn.send("Successfully connected to chat server".encode())
                self.clients.append(conn)
                self.clientsAddr[conn] = addr
                return conn
            else : 
                print("No valid Connection")

        except socket.timeout:
            # Closing server
            print("No Incoming Connection")
            print("Server Closed")
            self.soc.close()

        except KeyboardInterrupt:
            self.soc.close()
    ## .........

    ## Broadcast Message
    def _broadcast(self, msg, sender):
        try:
            if not msg or msg.lower() in ("exit", "q"):
                print(f"{self.clientsAddr[sender][0]}:{self.clientsAddr[sender][1]} requested to close connection")
                self.clients.remove(client)
                self.clientsAddr.pop(client)
                client.close()
            else:
                for client in self.clients:
                    if client != sender:
                        client.send(msg.encode())
        except:
            print("error in broadcasting")
    ## .........

    ## Handling Each Clients Seperately 
    def _handleClient(self, client):
        while True:
            try:
                msg = client.recv(1024).decode()
                self._broadcast(msg, client)
            except:
                self.clients.remove(client)
                self.clientsAddr.pop(client)
                client.close()
                break
    ## .........

    ## Chatting Method
    def online(self):
        self._startServer()
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                client = self._connectClient()
                if client:
                    executor.submit(self._handleClient, client)
                else:
                    break
    ## .........