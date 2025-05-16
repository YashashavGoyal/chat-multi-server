# Importing Modules
import socket
from concurrent.futures import ThreadPoolExecutor

DEFAULT_HOSTIP = '127.0.0.1'
DEFAULT_HOSTPORT = 8080

host_ip = input("Enter host ip: ") or DEFAULT_HOSTIP
input_port = int(input("Enter port number"))
host_port = input_port if input_port else DEFAULT_HOSTPORT

try:
    # Creating Socket And Running Server
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    soc.bind((host_ip, host_port))
    soc.listen(5)
except socket.error as err:
    print("Socket : ", err)

