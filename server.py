## Importing Modules
from concurrent.futures import ThreadPoolExecutor
import socket
import sys
## ........

## Configuring Host Details
DEFAULT_HOSTIP = '127.0.0.1'
DEFAULT_HOSTPORT = 8080

host_ip = input(f"Enter host ip (default {DEFAULT_HOSTIP}): ") or DEFAULT_HOSTIP
input_port = int(input(f"Enter port number (default {DEFAULT_HOSTPORT}): "))
host_port = input_port if input_port else DEFAULT_HOSTPORT
## ........

class SocketServer:

    ## Constructor
    def __init__(self, ip, port):
        self.host_ip = ip
        self.host_port = port
    ## ......

    ## Start Server method
    def startServer(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.soc.bind((self.host_ip, self.host_port))
            self.soc.listen(5)
        except socket.error as err:
            print("Socket failed with err : %s" %(err))
        else:
            print(f"Server is listening on {self.host_ip}:{self.host_port}")
            self.soc.settimeout(20)  # set waiting time 
    ## .........
    
    ## Client Connecting Method
    def connectClient(self):
        try:
            self.conn, self.addr = self.soc.accept()

            if self.conn:
                print(f"Connected to {self.addr}")
                self.conn.send("Successfully connected to server".encode())
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

    ## Sending Message Method
    def send_msg(self):
        try:
            while True:
                msg = input("You : ")
                if msg.lower() in ("exit", "q"):
                    self.conn.send(msg.encode())
                    self.conn.close()
                    print(f"Connection with {self.addr[0]}:{self.addr[1]} closed on your request")
                    break
                self.conn.send(msg.encode())
        except: 
            print("error in send msg")
    ## .........

    ## Receiving Message Method
    def recv_msg(self):
        try:
            while True:
                msg = self.conn.recv(1024).decode()
                if not msg or msg.lower() in ("exit", "q"):
                    print(f"{self.addr[0]}:{self.addr[1]} request to close connection\n")
                    self.conn.close()
                    break
                sys.stdout.write('\r' + ' ' * 80 + '\r')  # clear current input line
                print(f"{self.addr[0]}:{self.addr[1]} -: {msg}")
                # print(f"[Server]: {msg}")
                sys.stdout.write("You : ")
                sys.stdout.flush()
        except:
            print("error in recv_msg")
            self.soc.close()
    ## .........

    ## Chat Method
    def chat(self):
        pass