from concurrent.futures import ThreadPoolExecutor
from server import SocketServer

chats = []

def get_server_info():
    ## Configuring Host Details
    DEFAULT_HOSTNAME = "127.0.0.1"
    DEFAULT_HOSTPORT = 8080

    print("Enter Host Detail to run server : ")
    host_name = input(f"Host (default: {DEFAULT_HOSTNAME}) - ") or DEFAULT_HOSTNAME
    port = input(f"Port (default: {DEFAULT_HOSTPORT}) - ")
    host_port = int(port) if port else DEFAULT_HOSTPORT
    ## .........

    return (host_name, host_port)

def create_server():
    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            info = get_server_info()
            if info:
                newChat = SocketServer(info)
                executor.submit(newChat.online)
                chats.append(newChat)

            choice = input("Do you want to create a new chat server [y/n] : ")
            if choice.lower() != 'y':
                print("Server Manager shutting down.")
                break


create_server()