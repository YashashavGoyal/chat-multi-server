## Importing Modules
from concurrent.futures import ThreadPoolExecutor
import socket
## ........


class SocketServer:

    clients:list[socket.socket] = []
    clientsAddr:dict[socket.socket, tuple] = {}

    ## Constructor
    def __init__(self, host:tuple):
        self.host_ip = host[0]
        self.host_port = host[1]
    ## ......

    ## Start Server method
    def _startServer(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.soc.bind((self.host_ip, self.host_port))
            self.soc.listen(5)
        except socket.error as err:
            self.soc.close()  # ensure cleanup
            raise err  # let the manager catch it
        else:
            print(f"Server is listening on {self.host_ip}:{self.host_port}")
            # self.soc.settimeout(20)  # set waiting time 
    ## .........
    
    ## Client Connecting Method
    def _connectClient(self) -> socket.socket:
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

    ## Shutdown Server
    def _shutdown(self):
        print(f"Shuttind down server {self.host_ip}:{self.host_port}")

        for client in self.clients:
            try:
                client.send("Server is shutting down".encode())
                client.close()
            except:
                pass
        self.clients.clear()
        self.clientsAddr.clear()

        try:
            self.soc.close()
        except:
            pass

    ## Broadcast Message
    def _broadcast(self, msg, sender:socket.socket):
        msg = msg.strip() if msg else ""

        if msg.lower() in ("exit", "q"):
            print(f"{self.clientsAddr[sender][0]}:{self.clientsAddr[sender][1]} requested to close connection")
            sender.send("exit".encode())
            if sender in self.clients:
                self.clients.remove(sender)
            if sender in self.clientsAddr:
                self.clientsAddr.pop(sender)
            sender.close()
            return

        if not msg:
            return  # Empty messages should be ignored

        for client in self.clients:
            if client != sender:
                try:
                    client.send(msg.encode())
                except Exception as e:
                    print(f"Failed to send message to {self.clientsAddr.get(client)}: {e}")
    ## .........

    ## Handling Each Clients Seperately 
    def _handleClient(self, client:socket.socket):
            try:
                while True:
                    msg = client.recv(1024)
                    if not msg:
                        print(f"Client disconnected: {self.clientsAddr.get(client)}")
                        if client in self.clients:
                            self.clients.remove(client)
                        if client in self.clientsAddr:
                            self.clientsAddr.pop(client)
                        client.close()
                        break

                    decoded_msg = msg.decode().strip()
                    self._broadcast(decoded_msg, client)

            except (ConnectionResetError, ConnectionAbortedError, OSError) as err:
                print(f"Connection error with client {self.clientsAddr.get(client)}: {err}")

            finally:
                if client in self.clients:
                    self.clients.remove(client)
                self.clientsAddr.pop(client, None)
                client.close()

    ## .........

    ## Chatting Method
    def online(self):
        self._startServer()
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                while True:
                    client = self._connectClient()
                    if client:
                        executor.submit(self._handleClient, client)
                    else:
                        break
        except KeyboardInterrupt:
            print("Server shutting down.")
            self.soc.close()
            for client in self.clients:
                client.close()

    ## .........